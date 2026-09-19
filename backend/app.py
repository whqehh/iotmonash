"""
Flask Web Application & REST API
Serves:
- Real-time IoT Operations Dashboard
- Sensor Telemetry & Historical Data APIs
- Actuator Manual Override & Mode APIs
- Security Audit Log APIs
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

STATIC_DIR = Path(__file__).resolve().parent / "static"
app = Flask(__name__, static_folder=str(STATIC_DIR), static_url_path="")
app.config["SECRET_KEY"] = SECRET_KEY

@app.after_request
def security_headers_middleware(response):
    return apply_security_headers(response)

@app.errorhandler(Exception)
def generic_error_handler(e):
    app.logger.error(f"Internal error: {e}")
    log_security_event("INTERNAL_ERROR", "WARN", str(e)[:200], request.remote_addr or "127.0.0.1")
    return jsonify({
        "success": False,
        "error": "A secure internal error occurred."
    }), 500

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/api/sensors/latest", methods=["GET"])
def api_get_latest_sensors():
    data = get_latest_readings()
    return jsonify({"success": True, "sensors": data})

@app.route("/api/sensors/history", methods=["GET"])
def api_get_sensor_history():
    pos = request.args.get("position")
    try:
        limit = min(100, max(5, int(request.args.get("limit", 40))))
    except ValueError:
        limit = 40

    if pos and pos not in VALID_SENSOR_POSITIONS:
        return jsonify({"success": False, "error": f"Invalid sensor position: {pos}"}), 400

    history = get_sensor_history(pos, limit)
    return jsonify({"success": True, "count": len(history), "history": history})

@app.route("/api/sensors/poll-now", methods=["POST"])
def api_trigger_poll():
    if not check_rate_limit(request.remote_addr, max_requests=10, window_sec=30):
        return jsonify({"success": False, "error": "Rate limit exceeded."}), 429

    result = poll_and_record_all_sensors()
    return jsonify({
        "success": True,
        "message": "Immediate poll completed and persisted into MySQL sensor_data table.",
        "result": result
    })

@app.route("/api/actuators", methods=["GET"])
def api_get_actuators():
    states = get_actuator_states()
    return jsonify({"success": True, "actuators": states})

@app.route("/api/actuators/control", methods=["POST"])
def api_control_actuator():
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
    data = request.get_json(silent=True) or {}
    actuator = data.get("actuator")
    mode = data.get("mode")

    if actuator not in VALID_ACTUATORS:
        return jsonify({"success": False, "error": f"Invalid actuator: {actuator}"}), 400

    if mode == "AUTO":
        result = reset_to_auto(actuator)
        evaluate_automation_cycle()
        return jsonify(result)
    else:
        return jsonify({"success": False, "error": "Invalid mode request"}), 400

@app.route("/api/security/logs", methods=["GET"])
def api_get_security_logs():
    logs = get_recent_audit_logs(limit=25)
    return jsonify({"success": True, "logs": logs})

@app.route("/api/system/status", methods=["GET"])
def api_system_status():
    readings = get_latest_readings()
    actuators = get_actuator_states()
    return jsonify({
        "system": "Farm Defense Edge IoT",
        "db_status": "ONLINE (MySQL: farm_defense_db)",
        "monitored_sensors_count": len(readings),
        "actuators_count": len(actuators)
    })

def create_app():
    init_database_schema()
    start_poller()
    return app

if __name__ == "__main__":
    init_database_schema()
    start_poller()
    print(f"🚀 Farm Defense System running at http://127.0.0.1:{SERVER_PORT}")
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=False)
