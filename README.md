# 🛡️ NEMS: Network Event Monitoring System

<div align="center">
  <img src="https://img.shields.io/badge/python-3.10%2B-blue.svg" alt="Python Version" />
  <img src="https://img.shields.io/badge/flask-%23000.svg?style=flat&logo=flask&logoColor=white" alt="Flask" />
  <img src="https://img.shields.io/badge/Security-Scapy-red" alt="Scapy" />
  <img src="https://img.shields.io/badge/Database-SQLite-003B57" alt="SQLite" />
</div>

<br />

**NEMS** (Network Event Monitoring System) is a modular, lightweight, full-stack Intrusion Detection System (IDS) prototype. It intercepts raw network packets in real-time, analyzes metadata for security anomalies (like unauthorized port access or oversized packets), and visualizes the data through a high-performance web dashboard.

---

## 🚀 Key Features

- **⚡ Live Packet Ingestion:** Utilizes **Scapy** for raw socket sniffing at the Data Link and Network layers.
- **🚨 Intelligent Threat Analysis:** Rule-based engine that evaluates traffic and flags anomalies such as unauthorized port access (SSH/Telnet/RDP/SMB) and MTU (packet size) violations.
- **📊 Real-Time SOC Dashboard:** A Flask-powered "Security Operations Center" web interface with dynamic event prioritization, live heartbeat, grouping, and clean dark-mode aesthetics.
- **🗄️ Relational Persistence:** Fully structured **SQLite** database integration for historical event auditing, so no data is lost between sessions.
- **🔌 Multi-Node Testing:** Includes a dedicated `traffic_generator.py` script to seamlessly simulate network attacks or heavy traffic from client machines.

---

## 🏗️ Technical Architecture

NEMS follows a decoupled, modular MVP design. The heavy lifting of packet processing is separated from the UI rendering, allowing the system to scale efficiently.

| Component | Responsibility |
| :--- | :--- |
| **The Sensor (`monitor.py`)** | The "Ear" of the system. Captures raw network frames and extracts IP/TCP/UDP headers. |
| **The Brain (`analyzer.py`)** | The "Logic" layer. Compares packet metadata against configurable security rules. |
| **The Memory (`database.py`)** | The "Storage" layer. Manages local SQLite connection and ensures safe data insertion. |
| **The Interface (`web/`)** | The "Display" layer. A Flask server providing a RESTful JSON API and web dashboard. |

---

## ⚙️ Prerequisites

Before you begin, ensure you have the following installed to run NEMS successfully:
- **Python 3.10+**
- **pip** (Python package manager)
- **Npcap** (Windows only - required by Scapy for packet sniffing) or `tcpdump` (Linux).
- Administrator/Sudo privileges (necessary to sniff raw network sockets).

---

## 🛠️ Installation & Setup

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/network-monitor-system.git
cd network-monitor-system
```

**2. Create a virtual environment (Recommended)**
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

---

## 💻 Usage Guide

NEMS has three primary operational modes: The Packter Sniffer (Backend), the Dashboard (Web UI), and the testing script.

### 1. Start the Backend Sniffer
The backend must be run with elevated privileges to capture raw packets.
```bash
# Windows (Run Command Prompt as Administrator)
python run.py

# Linux / Mac
sudo python run.py
```
*Note: The backend will automatically create required `data` and `logs` directories and initialize the SQLite database on its first run.*

### 2. Start the Web Dashboard
Open a **new terminal window**, ensure your virtual environment is activated, and start the Flask web UI:
```bash
cd web
python dashboard.py
```
Once running, open your web browser and navigate to `http://127.0.0.1:5000` to view the live dashboard.

### 3. Generate Test Traffic
To verify the system is working, open a **third terminal** and deploy the built-in traffic generation tool. This script will simulate normal and malicious packets aimed at the monitor.
```bash
python traffic_generator.py
```

---

## 🔧 Configuration (`config.yaml`)

You can modify system thresholds entirely from the `config.yaml` file without altering code. 

```yaml
# Networking
monitor_ip: "192.168.0.163"  # Set to the IP address where run.py is executing

# Security Rules
rules:
  packet_size_threshold: 1500  # Will trigger an alert if a packet exceeds this byte size
  critical_ports:
    - 22    # SSH
    - 23    # Telnet
    - 3389  # RDP
    - 445   # SMB
```
*Any traffic targeting listed `critical_ports` or exceeding `packet_size_threshold` will trigger a security event in the database and glow RED on our dashboard.*

---

## 📂 Project Structure

```text
network-monitor-system/
├── app/                        # Backend Core Processing
│   ├── __init__.py             
│   ├── analyzer.py             # Security logic and threat classification
│   ├── database.py             # SQLite schema operations
│   ├── monitor.py              # Scapy-based sniffer
│   └── utils.py                # Formatting and IP resolution helpers
├── web/                        # Web Dashboard
│   ├── dashboard.py            # Flask web server and routing
│   └── templates/
│       └── index.html          # Modern UI with HTML/CSS/JS
├── data/                       # Persistent DB storage (Created on runtime)
├── logs/                       # Audit log files (Created on runtime)
├── config.yaml                 # Network settings and security rules
├── README.md                   # This documentation
├── requirements.txt            # Python module requirements
├── run.py                      # Backend sniffer entry point
└── traffic_generator.py        # Client-side multi-threading attack simulator
```

---

## ⚠️ Disclaimer
**For Educational Purposes Only.**
This project is built to demonstrate networking primitives, real-time data handling, and local web app integration. It is not intended for deployment in enterprise intrusion-prevention environments without extensive scaling modifications.