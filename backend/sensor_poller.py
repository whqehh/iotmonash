"""
Sensor Polling Service
Polls 4 edge sensor metrics every 1 minute:
1. Water Reservoir Level (0-1024)
2. Soil Moisture (0-1024)
3. Temperature / Sensor (0-1024)
4. DHT11 Humidity (%)

Validates and persists into MySQL `sensor_data` table.
"""

import time
import random
import threading
import logging
from typing import Dict, Any
from backend.config import POLL_INTERVAL_SECONDS
from backend.security import validate_sensor_payload
from backend.db import insert_sensor_reading, get_actuator_states
from backend.automation_engine import evaluate_automation_cycle

logger = logging.getLogger("SensorPoller")

# Realistic physical edge state simulation (0-1024 ADC range)
_state = {
    "water_level": 680.0,      # Analog level (0-1024), threshold < 500 triggers LED
    "soil_moisture": 450.0,    # Analog moisture (0-1024), starts < 500 to trigger pump
    "temperature": 318.0,      # Sensor value (0-1024), starts > 300 to trigger fan
    "humidity": 65.0           # Percentage
}

_running = False
_thread = None

def _read_physical_or_simulated_sensors() -> Dict[str, float]:
    """Read sensors from hardware or physics simulation."""
    global _state
    actuators = get_actuator_states()
    pump_on = actuators.get("pump", {}).get("state", False)
    fan_on = actuators.get("fan", {}).get("state", False)

    if pump_on:
        _state["soil_moisture"] = min(850.0, _state["soil_moisture"] + random.uniform(15.0, 30.0))
        _state["water_level"] = max(200.0, _state["water_level"] - random.uniform(4.0, 10.0))
    else:
        _state["soil_moisture"] = max(350.0, _state["soil_moisture"] - random.uniform(2.0, 6.0))

    if fan_on:
        _state["temperature"] = max(250.0, _state["temperature"] - random.uniform(3.0, 6.0))
        _state["humidity"] = max(40.0, _state["humidity"] - random.uniform(1.0, 2.5))
    else:
        _state["temperature"] = round(min(450.0, max(250.0, _state["temperature"] + random.uniform(-1.0, 2.0))), 1)
        _state["humidity"] = round(min(90.0, max(40.0, _state["humidity"] + random.uniform(-0.8, 1.2))), 1)

    return {
        "water_level": round(_state["water_level"], 2),
        "soil_moisture": round(_state["soil_moisture"], 2),
        "temperature": round(_state["temperature"], 2),
        "humidity": round(_state["humidity"], 2)
    }

def poll_and_record_all_sensors() -> Dict[str, Any]:
    """Execute a single synchronous poll cycle across all sensors."""
    raw_readings = _read_physical_or_simulated_sensors()
    results = {}

    for pos, raw_val in raw_readings.items():
        is_valid, err, clean_val = validate_sensor_payload(pos, raw_val)
        if is_valid:
            row_id = insert_sensor_reading(pos, clean_val)
            results[pos] = {
                "id": row_id,
                "value": clean_val,
                "status": "VALID_STORED"
            }
        else:
            results[pos] = {
                "value": raw_val,
                "status": "REJECTED_ANOMALY",
                "error": err
            }

    decision = evaluate_automation_cycle()

    return {
        "timestamp": time.time(),
        "readings": results,
        "automation": decision
    }

def _worker_loop():
    """Continuous background worker polling every 60s."""
    global _running
    logger.info(f"Sensor Poller Worker started. Polling every {POLL_INTERVAL_SECONDS} seconds.")
    
    try:
        poll_and_record_all_sensors()
    except Exception as e:
        logger.error(f"Error in initial poll: {e}")

    while _running:
        for _ in range(POLL_INTERVAL_SECONDS):
            if not _running:
                break
            time.sleep(1)
        
        if _running:
            try:
                poll_and_record_all_sensors()
            except Exception as e:
                logger.error(f"Polling cycle error: {e}")

def start_poller():
    """Start background sensor polling thread."""
    global _running, _thread
    if not _running:
        _running = True
        _thread = threading.Thread(target=_worker_loop, daemon=True)
        _thread.start()

def stop_poller():
    """Stop background sensor polling thread."""
    global _running
    _running = False
    if _thread:
        _thread.join(timeout=2)
