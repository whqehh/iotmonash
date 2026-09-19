"""
Configuration & Security Parameters for Farm Defense Edge IoT System
Compliant with OWASP Top 10 Database & Secure Software Development.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = Path(__file__).resolve().parent

# Load environment variables if present
load_dotenv(BASE_DIR / ".env")

# Database Configuration (OWASP A02: Externalized credentials)
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER", "hgroup3"),
    "password": os.getenv("DB_PASSWORD", "hgroup3"),
    "database": os.getenv("DB_NAME", "farm_defense_db"),
    "charset": "utf8mb4",
    "autocommit": True,
    "connect_timeout": 5
}

# Web Server Configuration
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", 5000))
SECRET_KEY = os.getenv("SECRET_KEY", "farm-defense-secret-key-edge-2026-safe-token")

# Sensor Polling Interval (Default 60s per hackathon specification)
POLL_INTERVAL_SECONDS = int(os.getenv("POLL_INTERVAL_SECONDS", 60))

# Valid Sensor Positions (Strict Whitelist for OWASP A03 / A08)
VALID_SENSOR_POSITIONS = {
    "water_level": {
        "unit": "raw",
        "min_valid": 0.0,
        "max_valid": 1024.0,
        "max_delta_per_min": 400.0,
        "description": "Water Reservoir Level"
    },
    "soil_moisture": {
        "unit": "raw",
        "min_valid": 0.0,
        "max_valid": 1024.0,
        "max_delta_per_min": 400.0,
        "description": "Substrate Soil Moisture"
    },
    "temperature": {
        "unit": "raw",
        "min_valid": 0.0,
        "max_valid": 1024.0,
        "max_delta_per_min": 350.0,
        "description": "DHT11 / Temperature Sensor"
    },
    "humidity": {
        "unit": "%",
        "min_valid": 0.0,
        "max_valid": 100.0,
        "max_delta_per_min": 50.0,
        "description": "DHT11 Ambient Humidity"
    }
}

# Valid Actuators (Strict Whitelist)
VALID_ACTUATORS = ["pump", "fan", "led"]

# Automation Decision Logic Thresholds
THRESHOLDS = {
    # Fan Motor Trigger
    "FAN_TEMP_HIGH": 300.0,           # Fan ON if reading > 300
    
    # Irrigation Pump Trigger
    "SOIL_MOISTURE_LOW": 500.0,       # Water Pump ON if soil < 500
    "SOIL_MOISTURE_TARGET": 650.0,    # Water Pump OFF when restored
    
    # Water Level & Alarm LED Trigger
    "WATER_LEVEL_LED_TRIGGER": 500.0, # Water level < 500 -> LED ON
    
    # Safety Watchdog
    "PUMP_MAX_RUNTIME_SEC": 45,       # Prevent motor burnout
    "PUMP_COOLDOWN_SEC": 15           # Cooldown between pump activations
}
