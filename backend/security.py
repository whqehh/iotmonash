"""
Security & Anomaly Detection Layer
Addresses:
- OWASP A01: Broken Access Control (Rate limiting, parameter whitelist)
- OWASP A03: Injection Defense (Strict schema validation & typing)
- OWASP A04: Insecure Design (Failsafe defaults & anomaly interlocks)
- OWASP A05: Security Misconfiguration (HTTP Security Headers)
- OWASP A08: Software and Data Integrity Failures (Sensor anomaly & corruption checks)
- OWASP A09: Security Logging & Monitoring Failures (Audit logger)
"""

import math
import time
from typing import Tuple, Optional, Dict, Any
from backend.config import VALID_SENSOR_POSITIONS, VALID_ACTUATORS
from backend.db import log_security_event

# In-memory track for rate of change anomaly detection & rate limiter
_last_known_readings: Dict[str, float] = {}
_client_request_history: Dict[str, list] = {}

class SensorAnomalyDetected(Exception):
    """Raised when incoming sensor reading violates physical sanity checks."""
    pass

def validate_sensor_payload(sensor_position: str, raw_value: Any) -> Tuple[bool, Optional[str], float]:
    """
    Validate incoming sensor data against strict whitelist and physical boundaries.
    Returns: (is_valid, error_reason, clean_numeric_value)
    """
    # 1. Check whitelist
    if not isinstance(sensor_position, str) or sensor_position not in VALID_SENSOR_POSITIONS:
        reason = f"OWASP A03/A08: Rejected unrecognized sensor position '{sensor_position}'"
        log_security_event("INVALID_SENSOR_KEY", "WARN", reason)
        return False, reason, 0.0

    # 2. Check numeric type
    try:
        val = float(raw_value)
    except (ValueError, TypeError):
        reason = f"OWASP A03: Non-numeric value received for '{sensor_position}': '{raw_value}'"
        log_security_event("TYPE_MISMATCH", "WARN", reason)
        return False, reason, 0.0

    # 3. Check NaN / Inf
    if math.isnan(val) or math.isinf(val):
        reason = f"OWASP A08: Corrupted float (NaN/Inf) received for '{sensor_position}'"
        log_security_event("CORRUPTED_DATA", "CRITICAL", reason)
        return False, reason, 0.0

    spec = VALID_SENSOR_POSITIONS[sensor_position]
    min_v = spec["min_valid"]
    max_v = spec["max_valid"]

    # 4. Out-of-bounds anomaly check
    if val < min_v or val > max_v:
        reason = f"ANOMALY: Value {val} for '{sensor_position}' out of range [{min_v}, {max_v}]"
        log_security_event("OUT_OF_BOUNDS", "ANOMALY", reason)
        return False, reason, val

    # 5. Rate-of-change / sudden spike anomaly check
    last_val = _last_known_readings.get(sensor_position)
    if last_val is not None:
        delta = abs(val - last_val)
        max_delta = spec.get("max_delta_per_min", 50.0)
        if delta > max_delta:
            reason = f"ANOMALY: Sudden spike detected for '{sensor_position}' (delta {delta:.2f} > limit {max_delta})"
            log_security_event("SUDDEN_SPIKE", "ANOMALY", reason)
            # Update reading so it doesn't stay permanently locked if the state really changed
            _last_known_readings[sensor_position] = val
            return False, reason, val

    # Reading passes all checks
    _last_known_readings[sensor_position] = val
    return True, None, round(val, 2)

def validate_actuator_command(actuator: str, state: Any, mode: str) -> Tuple[bool, Optional[str]]:
    """Validate actuator control parameters against strict constraints."""
    if actuator not in VALID_ACTUATORS:
        return False, f"Invalid actuator: {actuator}. Must be one of {VALID_ACTUATORS}"
    
    if mode not in ["AUTO", "MANUAL"]:
        return False, f"Invalid mode: {mode}. Must be 'AUTO' or 'MANUAL'"

    if not isinstance(state, (bool, int)):
        return False, "State must be boolean or integer (0/1)"

    return True, None

def check_rate_limit(client_ip: str, max_requests: int = 30, window_sec: int = 60) -> bool:
    """
    OWASP A01: Simple in-memory rate limiter to prevent DoS on actuator relay controls.
    """
    now = time.time()
    history = _client_request_history.get(client_ip, [])
    # Remove timestamps older than window
    history = [t for t in history if now - t < window_sec]
    
    if len(history) >= max_requests:
        log_security_event("RATE_LIMIT_EXCEEDED", "WARN", f"IP {client_ip} exceeded {max_requests} req/{window_sec}s", client_ip)
        return False
    
    history.append(now)
    _client_request_history[client_ip] = history
    return True

def apply_security_headers(response):
    """
    OWASP A05: Apply strict HTTP security headers to all web responses.
    """
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
        "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
        "img-src 'self' data:;"
    )
    return response
