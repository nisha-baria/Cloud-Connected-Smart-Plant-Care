# 🌱 Cloud-Connected Smart Plant Care & Automated Watering System
An industry-oriented IoT-to-Cloud telemetry and closed-loop actuation platform designed for automated plant hydration and remote environmental monitoring. Built using high-performance REST APIs, a realistic virtual sensor simulator, and a real-time web telemetry dashboard.

## 📌 Problem Statement & Architecture
Manual plant care often causes under-watering or over-watering, leading to resource wastage and degraded plant health. This system provides a cloud-native architecture that decouples physical/simulated sensing nodes from the telemetry ingestion layer, applies automated actuation logic based on dynamic thresholds, and visualizes live states.

```text
[ Virtual Sensor Simulator / ESP32 Node ]
                   │ (HTTP POST Telemetry Payload)
                   ▼
       [ FastAPI Cloud Backend ]
         │                   │
         ▼                   ▼
 [ SQLite Data Layer ]   [ Closed-Loop Actuation Engine ]
                             │
                             ▼
                 [ Virtual Pump / Relay State ]
                             │
                             ▼
                 [ Real-Time Web Dashboard ]

✨ Features
Virtual IoT Telemetry Simulator: Realistic environmental decay engine producing smooth fluctuations for soil moisture, ambient temperature, humidity, and simulated light without physical hardware.

Closed-Loop Automation Engine: Compares incoming telemetry against configurable thresholds to actuate watering cycles and trigger drying/wetting transitions.

RESTful API Service: Built with FastAPI to handle device registration, telemetry ingestion, historical logs, and manual overrides.

Real-Time Visual Dashboard: Interactive UI built with Vanilla JavaScript and Chart.js to monitor live metrics and historical trends.

Hardware Agnostic: Modular design that can seamlessly interface with an ESP32 microcontroller, capacitive soil sensor, and a 5V relay module.

📸 Screenshots & Telemetry Demonstration
1. Automated Watering Triggered (Below Threshold)
When soil moisture drops below the configured threshold (40%), the system marks the plant as "Needs Water" and toggles the pump state to ON.

2. Optimal System State (Idle / Above Threshold)
Once soil moisture reaches the optimal target (above 30%), the closed-loop engine deactivates the pump to prevent over-watering.

🛠️ Tech Stack

Backend: Python, FastAPI, Uvicorn, SQLite
Virtual Simulation: Python, Requests
Frontend: HTML5, CSS3, JavaScript, Chart.js
Embedded Hardware (Optional): C++, ESP32, Capacitive Soil Moisture Sensor v1.2, 5V Relay

📁 Repository Structure
Cloud-Connected-Smart-Plant-Care/
├── backend/
│   ├── app.py                # FastAPI endpoints & automation logic
│   ├── database.py           # SQLite schema & persistence helpers
│   └── requirements.txt      # Python dependencies
├── simulator/
│   └── sensor_sim.py         # Virtual IoT sensor generator
├── frontend/
│   ├── index.html            # Dashboard layout & markup
│   ├── style.css             # Responsive modern styling
│   └── app.js                # Real-time polling & Chart.js rendering
├── hardware/
│   └── esp32_firmware.ino    # Firmware for physical ESP32 node
├── screenshots/              # Visual proof and dashboard captures
├── .gitignore
├── LICENSE                   # MIT License
└── README.md

## 🚀 Quick Start

### 1. Setup & Install
```bash
cd Cloud-Connected-Smart-Plant-Care
pip install -r backend/requirements.txt
```

### 2. Run Backend (Terminal 1)
```bash
cd backend
uvicorn app:app --reload --port 8000
```

### 3. Run Sensor Simulator (Terminal 2)
```bash
python simulator/sensor_sim.py
```

### 4. Open Dashboard
Open `frontend/index.html` in the browser.

## 🌐 REST API Endpoints

* **POST** `/api/sensors/data` — Ingests sensor telemetry & evaluates threshold logic
* **GET** `/api/devices/{id}/latest` — Returns latest sensor readings & actuator state
* **GET** `/api/devices/{id}/history` — Retrieves chronological historical readings for charts
* **PUT** `/api/devices/{id}/threshold` — Updates the active moisture threshold value
* **POST** `/api/devices/{id}/water` — Triggers manual actuation override

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
