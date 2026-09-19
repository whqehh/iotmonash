"""
Unified Runner for Farm Defense Edge IoT System
Hour 0-6 Foundation Phase - HackMY IoT 2026

Starts:
1. MySQL Schema Verification & Table Health Check
2. Sensor Polling Worker (1-Minute Intervals with Anomaly Detection)
3. Autonomous Decision & Safety Engine (Dry-Run & Runaway Watchdog)
4. Operations Dashboard Web Server (http://127.0.0.1:5000)
"""

import sys
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from backend.config import SERVER_HOST, SERVER_PORT, DB_CONFIG, POLL_INTERVAL_SECONDS
from backend.db import init_database_schema, log_security_event
from backend.sensor_poller import start_poller, stop_poller
from backend.app import app

def main():
    print("=" * 70)
    print("  FARM DEFENSE AGENCY - EDGE IOT MISSION CONTROL")
    print("  Competition: HackMY IoT / MyEvolution Hackathon 2026")
    print("  Team: hGroup3 | Phase: Foundation Phase (Hour 0-6)")
    print("=" * 70)
    print(f"[*] Database       : MySQL ({DB_CONFIG['database']} @ {DB_CONFIG['host']}:{DB_CONFIG['port']})")
    print(f"[*] Polling Cycle  : Every {POLL_INTERVAL_SECONDS} seconds")
    print(f"[*] Monitored Pins : Water Level, Soil Moisture, DHT11 Temp, DHT11 Humidity")
    print(f"[*] Actuators      : Irrigation Pump, Cooling Fan Motor, Optical Alarm LED")
    print(f"[*] Security Standard: OWASP Top 10 Database & Secure SDLC Active")
    print("=" * 70)

    try:
        # 1. Initialize schema
        print("[*] Checking MySQL tables...")
        init_database_schema()
        print("    [+] Table `sensor_data` active.")
        print("    [+] Table `actuator_status` active.")
        print("    [+] Table `security_audit_logs` active.")

        # 2. Start background worker
        print("[*] Starting sensor polling background service...")
        start_poller()
        print("    [+] Background poller thread active.")

        log_security_event("SYSTEM_ONLINE", "INFO", "Farm Defense Edge server launched by operator.")

        # 3. Start web server
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
