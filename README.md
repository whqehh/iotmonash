# Farm Defense: Edge IoT Smart Irrigation & Actuator Control

A real-time edge IoT monitoring and automated irrigation control system built with Python, MySQL, and a modern web dashboard.

---

## 🚀 Features

- **Live Sensor Telemetry**: Continuous polling of 4 core edge sensors:
  - **Water Reservoir Level** (`water_level`)
  - **Substrate Soil Moisture** (`soil_moisture`)
  - **Ambient Temperature** (`temperature`)
  - **Ambient Humidity** (`humidity`)
- **Automated Decision Engine**:
  - **Irrigation Pump**: Activates automatically when Soil Moisture $< 500$.
  - **Cooling Fan Motor**: Activates automatically when Temperature $> 300$.
  - **Alarm / Status LED**: Activates automatically when Water Level $< 500$.
  - **Watchdog Protection**: 45-second continuous runtime limit to prevent motor burnout.
- **MySQL Database Persistence**:
  - Table `sensor_data` (`id`, `sensor_position`, `sensor_value`, `created_at`)
  - Table `actuator_status` (`actuator_name`, `state`, `mode`, `triggered_by`, `updated_at`)
  - Table `security_audit_logs` (`event_type`, `severity`, `details`, `source_ip`, `created_at`)
- **Modern Web Dashboard**: Real-time gauge meters, Chart.js time-series trend lines, manual actuator override controls, and a security audit event log.

---

## 🛠️ Prerequisites & Setup

### 1. Requirements
- Python 3.10+
- MySQL Server (running locally on port 3306)
- Python packages:
  ```bash
  pip install -r requirements.txt
  ```

### 2. Configure Database Credentials
Configure credentials in `backend/config.py` or create a `.env` file in the project root:
```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=hgroup3
DB_PASSWORD=hgroup3
DB_NAME=farm_defense_db
```

### 3. Initialize Database Schema
Create the required database tables and seed baseline telemetry:
```bash
python init_db.py
```

### 4. Run the Application
Start the background sensor poller, automation engine, and web server:
```bash
python run.py
```
Open your browser and navigate to:
**http://127.0.0.1:5000**

---

## 📂 Project Structure

```text
iotmonash/
├── backend/
│   ├── config.py              # Configuration, thresholds & whitelists
│   ├── db.py                  # Parameterized database access layer
│   ├── security.py            # Input validation & anomaly detection
│   ├── automation_engine.py   # Decision logic & safety interlocks
│   ├── sensor_poller.py       # Autonomous 1-minute sensor polling service
│   ├── app.py                 # REST API endpoints & static server
│   └── static/                # Modern glassmorphism dashboard UI
│       ├── index.html
│       ├── css/style.css
│       └── js/dashboard.js
├── init_db.py                 # Database table creator & seed script
├── requirements.txt           # Dependency requirements
├── run.py                     # Unified edge IoT application runner
├── .gitignore
└── README.md
```
