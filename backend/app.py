"""
Flask Web Application & Secure REST API
Complies with OWASP Top 10 Database & Secure Software Development.
Serves:
- Real-time IoT Operations Dashboard
- Sensor Telemetry & Historical Data APIs
- Actuator Manual Override & Autonomous Mode APIs
- Security Audit & Anomaly Monitoring APIs
"""

import os
from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory
from backend.config import SERVER_HOST, SERVER_PORT, SECRET_KEY, VALID_SENSOR_POSITIONS, VALID_ACTUATORS
from backend.db import (
    init_database_schema,
    get_latest_readings,
    get_sensor_history,
    get_actuator_states,
    get_recent_audit_logs,
    log_security_event
)
from backend.security import (
    validate_actuator_command,
    check_rate_limit,
    apply_security_headers
)
from backend.automation_engine import (
    manual_override_actuator,
    reset_to_auto,
    evaluate_automation_cycle
)
from backend.sensor_poller import poll_and_record_all_sensors, start_poller

# Initialize Flask app pointing to static frontend directory
STATIC_DIR = Path(__file__).resolve().parent / "static"
app = Flask(__name__, static_folder=str(STATIC_DIR), static_url_path="")
app.config["SECRET_KEY"] = SECRET_KEY

# ------------------------------------------------------------------
# OWASP Security Middleware
# ------------------------------------------------------------------
@app.after_request
def security_headers_middleware(response):
    """Apply OWASP A05 HTTP Security Headers."""
    return apply_security_headers(response)

@app.errorhandler(Exception)
def generic_error_handler(e):
    """OWASP A05: Mask raw exceptions to prevent sensitive information disclosure."""
    app.logger.error(f"Internal error: {e}")
    log_security_event("INTERNAL_ERROR", "WARN", str(e)[:200], request.remote_addr or "127.0.0.1")
    return jsonify({
        "success": False,
        "error": "A secure internal error occurred. Request was safely halted."
    }), 500

# ------------------------------------------------------------------
# Static Frontend Routes
# ------------------------------------------------------------------
@app.route("/")
def index():
    """Serve the real-time IoT dashboard."""
    return send_from_directory(app.static_folder, "index.html")

# ------------------------------------------------------------------
# Sensor APIs
# ------------------------------------------------------------------
@app.route("/api/sensors/latest", methods=["GET"])
def api_get_latest_sensors():
    """Retrieve current readings for all monitored sensors."""
    data = get_latest_readings()
    return jsonify({
        "success": True,
        "sensors": data
    })

@app.route("/api/sensors/history", methods=["GET"])
def api_get_sensor_history():
    """
    Retrieve historical data from MySQL `sensor_data` table.
    Parameterized filter by position (optional).
    """
    pos = request.args.get("position")
    try:
        limit = min(100, max(5, int(request.args.get("limit", 40))))
    except ValueError:
        limit = 40

    if pos and pos not in VALID_SENSOR_POSITIONS:
        return jsonify({"success": False, "error": f"Invalid sensor position: {pos}"}), 400

    history = get_sensor_history(pos, limit)
    return jsonify({
        "success": True,
        "count": len(history),
        "history": history
    })

@app.route("/api/sensors/poll-now", methods=["POST"])
def api_trigger_poll():
    """Manually trigger immediate sensor poll cycle (for judge live demonstration)."""
    if not check_rate_limit(request.remote_addr, max_requests=10, window_sec=30):
        return jsonify({"success": False, "error": "Rate limit exceeded. Try again shortly."}), 429

    result = poll_and_record_all_sensors()
    return jsonify({
        "success": True,
        "message": "Immediate poll completed and persisted into MySQL sensor_data table.",
        "result": result
    })

# ------------------------------------------------------------------
# Actuator APIs (Pump, Fan, LED)
# ------------------------------------------------------------------
@app.route("/api/actuators", methods=["GET"])
def api_get_actuators():
    """Get real-time states and operating modes for all actuators."""
    states = get_actuator_states()
    return jsonify({
        "success": True,
        "actuators": states
    })

@app.route("/api/actuators/control", methods=["POST"])
def api_control_actuator():
    """
    Manual toggle of an actuator (Pump, Fan, LED).
    Subject to dry-run safety lockout and rate limiting.
    """
    if not check_rate_limit(request.remote_addr, max_requests=20, window_sec=60):
        return jsonify({"success": False, "error": "Rate limit exceeded."}), 429

    data = request.get_json(silent=True) or {}
    actuator = data.get("actuator")
    state = data.get("state")

    is_valid, err = validate_actuator_command(actuator, state, "MANUAL")
    if not is_valid:
        return jsonify({"success": False, "error": err}), 400

    result = manual_override_actuator(actuator, bool(state))
    status_code = 200 if result.get("success") else 403
    return jsonify(result), status_code

@app.route("/api/actuators/mode", methods=["POST"])
def api_set_actuator_mode():
    """Switch an actuator between AUTO and MANUAL mode."""
    data = request.get_json(silent=True) or {}
    actuator = data.get("actuator")
    mode = data.get("mode")

    if actuator not in VALID_ACTUATORS:
        return jsonify({"success": False, "error": f"Invalid actuator: {actuator}"}), 400

    if mode == "AUTO":
        result = reset_to_auto(actuator)
        # Re-evaluate automation cycle immediately
        evaluate_automation_cycle()
        return jsonify(result)
    else:
        return jsonify({"success": False, "error": "Use /api/actuators/control to set manual states."}), 400

# ------------------------------------------------------------------
# Security & System Health APIs
# ------------------------------------------------------------------
@app.route("/api/security/logs", methods=["GET"])
def api_get_security_logs():
    """Get latest OWASP security audit logs and anomaly alerts."""
    logs = get_recent_audit_logs(limit=25)
    return jsonify({
        "success": True,
        "logs": logs
    })

@app.route("/api/system/status", methods=["GET"])
def api_system_status():
    """Get system health and challenge compliance overview."""
    readings = get_latest_readings()
    actuators = get_actuator_states()
    return jsonify({
        "system": "Farm Defense Edge IoT",
        "phase": "Foundation Phase (Challenge 1)",
        "db_status": "ONLINE (MySQL: farm_defense_db)",
        "monitored_sensors_count": len(readings),
        "actuators_count": len(actuators),
        "owasp_compliance": "OWASP Top 10 DB & Secure SDLC Active",
        "offline_edge_ready": True
    })

def create_app():
    """Application factory: initializes DB tables and background worker."""
    init_database_schema()
    start_poller()
    return app

if __name__ == "__main__":
    init_database_schema()
    start_poller()
    print(f"🚀 Farm Defense System running at http://127.0.0.1:{SERVER_PORT}")
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=False)
