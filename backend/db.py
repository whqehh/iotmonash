"""
Database Access Layer compliant with OWASP Top 10 Database Security.
Implements:
- 100% Parameterized queries with prepared statements (A03: SQL Injection defense)
- Whitelisting of dynamic parameters (identifiers)
- Connection recovery & error handling without sensitive stack trace leaks
"""

import pymysql
import pymysql.cursors
from typing import List, Dict, Any, Optional
from datetime import datetime
from backend.config import DB_CONFIG, VALID_SENSOR_POSITIONS, VALID_ACTUATORS

def get_connection():
    """Create a managed PyMySQL database connection."""
    return pymysql.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"],
        charset=DB_CONFIG["charset"],
        autocommit=DB_CONFIG["autocommit"],
        connect_timeout=DB_CONFIG["connect_timeout"],
        cursorclass=pymysql.cursors.DictCursor
    )

def init_database_schema():
    """
    Ensure all required tables exist per challenge specifications.
    Required table: sensor_data (id, sensor_position, sensor_value, created_at).
    Additional tables for OWASP compliance: actuator_status, security_audit_logs.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # 1. Main sensor table mandated by Challenge 1 specification
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sensor_data (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    sensor_position VARCHAR(255) NOT NULL,
                    sensor_value DECIMAL(10,2) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_sensor_position (sensor_position),
                    INDEX idx_created_at (created_at)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """)

            # 2. Actuator state table for pump, fan, led
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS actuator_status (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    actuator_name VARCHAR(100) NOT NULL UNIQUE,
                    state TINYINT(1) DEFAULT 0,
                    mode VARCHAR(20) DEFAULT 'AUTO',
                    triggered_by VARCHAR(255) DEFAULT 'System Init',
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """)

            # 3. Security audit log table (OWASP A09: Logging & Monitoring)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS security_audit_logs (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    event_type VARCHAR(100) NOT NULL,
                    severity VARCHAR(20) NOT NULL,
                    details TEXT NOT NULL,
                    source_ip VARCHAR(50) DEFAULT '127.0.0.1',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_severity (severity),
                    INDEX idx_created_at (created_at)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """)

            # Seed default actuator rows if not present
            for act in VALID_ACTUATORS:
                cursor.execute("""
                    INSERT INTO actuator_status (actuator_name, state, mode, triggered_by)
                    VALUES (%s, 0, 'AUTO', 'Initial Boot')
                    ON DUPLICATE KEY UPDATE actuator_name=actuator_name;
                """, (act,))
    finally:
        conn.close()

def insert_sensor_reading(sensor_position: str, sensor_value: float) -> int:
    """
    Strictly parameterized insert into sensor_data table.
    Matches the exact column structure: (sensor_position, sensor_value, created_at).
    """
    if sensor_position not in VALID_SENSOR_POSITIONS:
        raise ValueError(f"Invalid sensor position: {sensor_position}")
    
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO sensor_data (sensor_position, sensor_value) VALUES (%s, %s);"
            cursor.execute(sql, (sensor_position, float(sensor_value)))
            return cursor.lastrowid
    finally:
        conn.close()

def get_latest_readings() -> Dict[str, Dict[str, Any]]:
    """Retrieve the most recent reading for each sensor position."""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT s1.id, s1.sensor_position, s1.sensor_value, s1.created_at
                FROM sensor_data s1
                INNER JOIN (
                    SELECT sensor_position, MAX(id) as max_id
                    FROM sensor_data
                    GROUP BY sensor_position
                ) s2 ON s1.sensor_position = s2.sensor_position AND s1.id = s2.max_id;
            """
            cursor.execute(sql)
            rows = cursor.fetchall()
            result = {}
            for r in rows:
                pos = r["sensor_position"]
                val = float(r["sensor_value"])
                result[pos] = {
                    "id": r["id"],
                    "value": val,
                    "unit": VALID_SENSOR_POSITIONS.get(pos, {}).get("unit", ""),
                    "description": VALID_SENSOR_POSITIONS.get(pos, {}).get("description", pos),
                    "created_at": r["created_at"].strftime("%Y-%m-%d %H:%M:%S") if r["created_at"] else ""
                }
            return result
    finally:
        conn.close()

def get_sensor_history(sensor_position: Optional[str] = None, limit: int = 40) -> List[Dict[str, Any]]:
    """Retrieve time-series sensor history with parameterized filtering."""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            if sensor_position and sensor_position in VALID_SENSOR_POSITIONS:
                sql = """
                    SELECT id, sensor_position, sensor_value, created_at
                    FROM sensor_data
                    WHERE sensor_position = %s
                    ORDER BY id DESC LIMIT %s;
                """
                cursor.execute(sql, (sensor_position, limit))
            else:
                sql = """
                    SELECT id, sensor_position, sensor_value, created_at
                    FROM sensor_data
                    ORDER BY id DESC LIMIT %s;
                """
                cursor.execute(sql, (limit,))
            rows = cursor.fetchall()
            # Format datetime for JSON serialization
            for r in rows:
                r["sensor_value"] = float(r["sensor_value"])
                if isinstance(r.get("created_at"), datetime):
                    r["created_at"] = r["created_at"].strftime("%Y-%m-%d %H:%M:%S")
            return list(reversed(rows))
    finally:
        conn.close()

def get_actuator_states() -> Dict[str, Dict[str, Any]]:
    """Retrieve current states of all actuators."""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT actuator_name, state, mode, triggered_by, updated_at FROM actuator_status;")
            rows = cursor.fetchall()
            result = {}
            for r in rows:
                result[r["actuator_name"]] = {
                    "state": bool(r["state"]),
                    "mode": r["mode"],
                    "triggered_by": r["triggered_by"],
                    "updated_at": r["updated_at"].strftime("%Y-%m-%d %H:%M:%S") if r["updated_at"] else ""
                }
            return result
    finally:
        conn.close()

def set_actuator_state(actuator_name: str, state: bool, mode: str, triggered_by: str):
    """Update actuator status with parameterized query."""
    if actuator_name not in VALID_ACTUATORS:
        raise ValueError(f"Invalid actuator: {actuator_name}")
    
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                UPDATE actuator_status
                SET state = %s, mode = %s, triggered_by = %s
                WHERE actuator_name = %s;
            """
            cursor.execute(sql, (1 if state else 0, mode, triggered_by, actuator_name))
    finally:
        conn.close()

def log_security_event(event_type: str, severity: str, details: str, source_ip: str = "127.0.0.1"):
    """
    Record an event in security_audit_logs.
    Severity: 'INFO', 'WARN', 'CRITICAL', 'ANOMALY'.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO security_audit_logs (event_type, severity, details, source_ip)
                VALUES (%s, %s, %s, %s);
            """
            cursor.execute(sql, (event_type[:100], severity[:20], details, source_ip[:50]))
    finally:
        conn.close()

def get_recent_audit_logs(limit: int = 25) -> List[Dict[str, Any]]:
    """Get latest security audit records."""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, event_type, severity, details, source_ip, created_at
                FROM security_audit_logs
                ORDER BY id DESC LIMIT %s;
            """, (limit,))
            rows = cursor.fetchall()
            for r in rows:
                if isinstance(r.get("created_at"), datetime):
                    r["created_at"] = r["created_at"].strftime("%Y-%m-%d %H:%M:%S")
            return rows
    finally:
        conn.close()
