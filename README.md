# 🛡️ NEMS: Network Event Monitoring System

![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=flat&logo=flask&logoColor=white)
![Scapy](https://img.shields.io/badge/Security-Scapy-red)
![License](https://img.shields.io/badge/license-MIT-green)

**NEMS** is a modular, full-stack Network Intrusion Detection System (IDS) designed to provide real-time visibility into network traffic. It sniffs raw packets, analyzes them for security threats, and visualizes the data through a modern, responsive web dashboard.

---

## 🌟 Key Features

- **⚡ Real-Time Sniffing:** Leverages the **Scapy** library to intercept and parse raw packets at the Data Link and Network layers.
- **🚨 Threat Detection:** Automatically flags unauthorized access attempts on sensitive ports (SSH, Telnet, RDP) as **CRITICAL**.
- **📊 Bandwidth Monitoring:** Identifies potential data exfiltration or heavy streaming by flagging packets exceeding MTU limits.
- **🖥️ Live Dashboard:** A Flask-powered "Security Operations Center" (SOC) interface with a pulsing status indicator and event prioritization.
- **🗄️ Persistent Logging:** Dual-storage system using **SQLite** for structured data and flat-file logs for audit trails.

---

## 🏗️ Technical Architecture

NEMS is built with a decoupled architecture to ensure stability and low-latency packet processing.

| Component | Technology | Responsibility |
| :--- | :--- | :--- |
| **Ingestion** | Scapy (Python) | Raw packet capture and header extraction. |
| **Analysis** | Rule-based Engine | Logic for prioritizing and filtering network events. |
| **Storage** | SQLite | Relational storage for historical event analysis. |
| **Interface** | Flask / Jinja2 | Web server and dynamic template rendering. |

---

## 📁 Project Structure

```text
network-monitor-system/
├── app/                # Backend Logic
│   ├── analyzer.py     # Threat detection rules
│   ├── database.py     # SQLite schema and queries
│   ├── monitor.py      # Scapy sniffer implementation
│   └── utils.py        # Logging and network utilities
├── web/                # Frontend
│   ├── dashboard.py    # Flask routing
│   └── templates/      # HTML/CSS UI
├── data/               # Persistent SQLite storage
├── logs/               # Raw text log backups
├── config.yaml         # Externalized system configuration
├── requirements.txt    # Project dependencies
└── run.py              # Main system entry point