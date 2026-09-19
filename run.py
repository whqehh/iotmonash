"""
Unified Runner for Farm Defense Edge IoT System
Starts:
1. MySQL Schema Verification & Table Health Check
2. Sensor Polling Worker (1-Minute Intervals with Anomaly Detection)
3. Autonomous Decision & Safety Engine (Pump < 500, Fan > 300, LED < 500)
4. Operations Dashboard Web Server (http://127.0.0.1:5000)
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from backend.config import SERVER_HOST, SERVER_PORT, DB_CONFIG, POLL_INTERVAL_SECONDS
from backend.db import init_database_schema, log_security_event
from backend.sensor_poller import start_poller, stop_poller
from backend.app import app

def main():
    print("=" * 70)
    print("  FARM DEFENSE AGENCY - EDGE IOT MISSION CONTROL")
    print("=" * 70)
    print(f"[*] Database       : MySQL ({DB_CONFIG['database']} @ {DB_CONFIG['host']}:{DB_CONFIG['port']})")
    print(f"[*] Polling Cycle  : Every {POLL_INTERVAL_SECONDS} seconds")
    print(f"[*] Monitored Pins : Water Level, Soil Moisture, DHT11 Temp, DHT11 Humidity")
    print(f"[*] Actuators      : Irrigation Pump, Cooling Fan Motor, Optical Alarm LED")
    print("=" * 70)

    try:
        print("[*] Checking MySQL tables...")
        init_database_schema()
        print("    [+] Table `sensor_data` active.")
        print("    [+] Table `actuator_status` active.")
        print("    [+] Table `security_audit_logs` active.")

        print("[*] Starting sensor polling background service...")
        start_poller()
        print("    [+] Background poller thread active.")

        log_security_event("SYSTEM_ONLINE", "INFO", "Farm Defense Edge server launched by operator.")

        print(f"\n[>>>] Operations Dashboard LIVE: http://127.0.0.1:{SERVER_PORT}")
        print("[>>>] Press CTRL+C to halt gracefully.\n")
        app.run(host=SERVER_HOST, port=SERVER_PORT, debug=False, use_reloader=False)

    except KeyboardInterrupt:
        print("\n[*] Shutting down edge services...")
        stop_poller()
        print("[*] Edge system halted cleanly.")
    except Exception as e:
        print(f"\n[!] Critical Startup Failure: {e}")
        stop_poller()
        sys.exit(1)

if __name__ == "__main__":
    main()
