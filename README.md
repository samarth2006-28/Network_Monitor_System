# 🛡️ NEMS: Network Event Monitoring System

![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=flat&logo=flask&logoColor=white)
![Scapy](https://img.shields.io/badge/Security-Scapy-red)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57)

**NEMS** (Network Event Monitoring System) is a modular, full-stack Intrusion Detection System (IDS) prototype. It intercepts raw network packets, analyzes metadata for security anomalies, and visualizes the data through a high-performance web dashboard.

---

## 🚀 Key Features

- **⚡ Live Packet Ingestion:** Utilizes **Scapy** for raw socket sniffing at the Data Link and Network layers.
- **🚨 Intelligent Threat Analysis:** Rule-based engine that flags unauthorized port access (SSH/Telnet) and MTU violations.
- **📊 Real-Time SOC Dashboard:** A Flask-powered "Security Operations Center" interface with dynamic event prioritization and a "System Live" heartbeat.
- **🗄️ Relational Persistence:** Fully structured **SQLite** database integration for historical event auditing.
- **🔌 Multi-Node Testing:** Includes a dedicated Traffic Generator script to simulate network attacks from a client machine.

---

## 🏗️ Technical Architecture

NEMS follows a decoupled, modular design to ensure that packet processing is not delayed by the UI rendering.

| Component | Responsibility |
| :--- | :--- |
| **The Sensor (`monitor.py`)** | The "Ear" of the system. Captures raw frames and extracts IP/TCP/UDP headers. |
| **The Brain (`analyzer.py`)** | The "Logic" layer. Compares packet metadata against security rules in `config.yaml`. |
| **The Memory (`database.py`)** | The "Storage" layer. Manages SQL connections and ensures data integrity. |
| **The Interface (`web/`)** | The "Display" layer. A Flask server that provides a RESTful view of the database. |

---

## 📂 Project Structure

```text
network-monitor-system/
├── app/                        # Backend Core
│   ├── __init__.py             # Python package marker
│   ├── analyzer.py             # Security logic and threat classification
│   ├── database.py             # SQLite schema and data insertion
│   ├── monitor.py              # Scapy-based raw packet sniffer
│   └── utils.py                # Terminal coloring and IP resolution
├── web/                        # Web Dashboard
│   ├── dashboard.py            # Flask server routing
│   └── templates/
│       └── index.html          # Modern Dark-Mode UI with CSS animations
├── data/                       # Persistent database storage
├── logs/                       # Plain-text audit log backups
├── config.yaml                 # System settings and security thresholds
├── README.md                   # Project documentation
├── requirements.txt            # Dependency list
├── run.py                      # Main entry point (Backend start)
└── traffic_generator.py        # Client-side testing tool