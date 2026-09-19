"""
Database Initializer for HackMY IoT 2026: Challenge 1 "Save the Farm"
Creates required tables and seeds baseline data in MySQL `farm_defense_db`.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from backend.config import DB_CONFIG
from backend.db import (
    init_database_schema,
    insert_sensor_reading,
    log_security_event,
    get_connection
)

def run_setup():
    print("=" * 65)
    print("  FARM DEFENSE AGENCY - WELCOME BRIEFING")
    print("  Initializing Database & Security Subsystems")
    print("=" * 65)
    print(f"[*] Target Database : {DB_CONFIG['database']} @ {DB_CONFIG['host']}:{DB_CONFIG['port']}")
    print(f"[*] Target User     : {DB_CONFIG['user']}")

    try:
        # 1. Initialize schema
        print("[*] Creating / Verifying MySQL Tables...")
        init_database_schema()
        print("    [+] Table `sensor_data` verified (id, sensor_position, sensor_value, created_at)")
        print("    [+] Table `actuator_status` verified (pump, fan, led)")
        print("    [+] Table `security_audit_logs` verified (OWASP A09 compliant)")

        # 2. Seed initial baseline records so dashboard displays real data immediately
        print("[*] Seeding initial sensor readings...")
        seed_data = [
            ("water_level", 650.00),
            ("soil_moisture", 450.00),
            ("temperature", 310.00),
            ("humidity", 65.00)
        ]
        for pos, val in seed_data:
            row_id = insert_sensor_reading(pos, val)
            print(f"    [+] {pos:15} = {val:6.2f} (Record #{row_id})")

        # 3. Log initial security event
        log_security_event("SYSTEM_BOOT", "INFO", "Farm Defense Edge IoT initialized. All safety interlocks armed.")
        print("[*] Security Audit Logger initialized.")

        print("=" * 65)
        print("[SUCCESS] DATABASE INITIALIZATION COMPLETED SUCCESSFULLY!")
        print("=" * 65)

    except Exception as e:
        print(f"\n[!] ERROR initializing database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_setup()
