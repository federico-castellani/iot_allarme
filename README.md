# IoT Alarm System with Micro:bit

A comprehensive IoT alarm system using BBC micro:bit devices for movement detection, Flask web interface for remote control, and real-time monitoring with InfluxDB and Grafana.

## System Overview

This project implements a distributed alarm system where:
- Two BBC micro:bit devices communicate via radio
- A PIR sensor detects movement
- IR remote provides local control
- Flask web app enables remote control via browser
- InfluxDB stores time-series sensor data
- Grafana provides real-time visualization dashboards

## Architecture

```
Micro:bit (Controller) ←→ Radio ←→ Micro:bit (Serial Bridge)
       ↓                                    ↓
   PIR Sensor                          Serial Port
   IR Remote                               ↓
   LCD Display                       lettura.py ←→ InfluxDB
   LEDs                                    ↑           ↓
                                    Flask App ←→ Grafana
```

## Hardware Components

### Micro:bit Controller (`Microbit/python_movimento.py`)
- **Movement Detection**: PIR sensor connected to pin 0
- **IR Remote Control**: IR receiver on pin 1 for alarm control
- **Visual Feedback**: 
  - LCD display showing alarm status
  - LED indicators (Green=OFF, Yellow=READY, Red=ALARM)
- **Radio Communication**: Sends status updates to second micro:bit

### Micro:bit Serial Bridge (`Microbit/python_caricamento.py`)
- **Radio Receiver**: Receives status from controller micro:bit
- **Serial Output**: Forwards data to computer via USB

## Software Components

### Data Collection (`lettura.py`)
Reads serial data from micro:bit and stores in InfluxDB:
- Monitors `/dev/serial/by-id/...` for micro:bit connection
- Parses alarm status messages (ON/OFF/SILENCED/MOVEMENT)
- Writes timestamped data to InfluxDB with authentication token

### Flask Web Application
- **Application Factory** (`Iot_Flask/flaskr/__init__.py`): Creates Flask app with blueprint registration
- **Dashboard Blueprint** (`Iot_Flask/flaskr/Dashboard.py`): 
  - `/dashboard` - Main control interface
  - `/get_last_status` - API endpoint for current alarm state
  - Serial communication to control alarm remotely

### Web Interface (`Iot_Flask/flaskr/templates/Dashboard.html`)
- Toggle switch for alarm activation/deactivation
- Embedded Grafana dashboards for real-time monitoring
- AJAX calls to Flask API for status updates

### Database & Monitoring
- **InfluxDB**: Time-series database for sensor data storage
- **Grafana**: Real-time dashboards and data visualization
- **Docker Compose** (`docker-compose.yml`): Orchestrates InfluxDB and Grafana containers

## Installation & Setup

### 1. Hardware Setup
- Connect PIR sensor to micro:bit pin 0
- Connect IR receiver to micro:bit pin 1
- Connect LCD display to micro:bit I2C pins
- Flash `python_movimento.py` to controller micro:bit
- Flash `python_caricamento.py` to bridge micro:bit

### 2. Software Dependencies
```bash
pip install flask influxdb-client pyserial
```

### 3. Database Setup
```bash
# Start InfluxDB and Grafana
docker-compose up -d

# Configure InfluxDB authentication token in 'token' file
```

### 4. Running the System

**Start data collection** (requires sudo for serial access):
```bash
sudo python3 lettura.py
```

**Start Flask web interface** (requires sudo for serial control):
```bash
cd Iot_Flask
sudo python3 -m flask --app flaskr run --host=0.0.0.0 --port=5000
```

## Usage

### Local Control
- **IR Remote**:
- **OK**: Silences the alarm
- **#**: Cleans the inserted numbers on the LCD
- **8086**: Is used to switch the alarm status (ON/OFF)

### Remote Control
- Access web interface at `http://localhost:5000/dashboard`
- Use toggle switch to activate/deactivate alarm
- Monitor real-time status and historical data via Grafana dashboards

### Alarm States
- **ON** (Green LED):  Armed, waiting for movement
- **ALARM** (Yellow LED): Movement detected, alarm triggered
- **OFF** (Red LED): System inactive
- **SILENCED**: Alarm acknowledged

## System Requirements

### Linux Permissions
Both `lettura.py` and the Flask app require `sudo` privileges because they access serial ports:
- `/dev/serial/by-id/...` (micro:bit USB connection)
- `/dev/ttyACM1` (alternative serial device)

Serial port access requires elevated permissions for direct hardware communication.

### Port Configuration
- Flask app: `http://localhost:5000`
- InfluxDB: `http://localhost:8086`
- Grafana: `http://localhost:3000`

## Data Flow

1. PIR sensor detects movement → Micro:bit controller
2. Controller processes event → Updates LCD/LEDs → Sends radio message
3. Bridge micro:bit receives radio → Outputs to serial
4. `lettura.py` reads serial → Writes to InfluxDB
5. Grafana queries InfluxDB → Displays real-time data
6. Flask app reads serial + controls system via web interface

## Troubleshooting

- **Serial Permission Denied**: Run with `sudo`
- **Micro:bit Not Found**: Check USB connection and device path in code
- **Database Connection**: Verify InfluxDB container is running
- **Radio Communication**: Ensure both micro:bits use same radio group

## Credits
- **LCD library**: By **[shaoziyang](https://github.com/shaoziyang)** (https://github.com/shaoziyang/microbit-lib.git)
- **IR Receiver**: By **[inexglobal](https://github.com/inexglobal)** (https://github.com/inexglobal/irm.git)

## License

[Add your license information here]
