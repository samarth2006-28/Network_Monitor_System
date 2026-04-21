from flask import Flask, jsonify, render_template
from datetime import datetime
from app.database import get_recent_events
from app.analyzer import SYSTEM_STATUS, packet_timestamps

app = Flask(__name__)

def get_dashboard_data(limit=50):
    """Builds a dashboard payload shared by HTML and API routes."""
    pps = 0.0
    if len(packet_timestamps) > 2:
        time_span = packet_timestamps[-1] - packet_timestamps[0]
        pps = round(len(packet_timestamps) / time_span, 1) if time_span > 0 else 0

    events = get_recent_events(limit=limit)
    total_logs = len(events)
    critical_count = sum(1 for e in events if "CRITICAL" in e['type'])
    warning_count = sum(1 for e in events if "WARNING" in e['type'])
    info_count = total_logs - critical_count - warning_count
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    avg_score = 0
    if total_logs > 0:
        avg_score = int((sum(e['score'] for e in events) / total_logs) * 100)

    high_risk = max((int(e['score'] * 100) for e in events), default=0)
    last_profile = "NONE"
    profile_map = {
        "INFO": "Option 1 - INFO Baseline",
        "WARNING": "Option 2 - WARNING Burst",
        "CRITICAL": "Option 3 - CRITICAL Probe",
        "CONGESTION": "Option 4 - CONGESTION Storm",
    }

    for event in events:
        details = event.get("details", "")
        if "[PROFILE:" in details:
            try:
                token = details.split("[PROFILE:", 1)[1].split("]", 1)[0].strip().upper()
                last_profile = profile_map.get(token, token)
                break
            except Exception:
                continue

    return {
        "events": events,
        "system_status": SYSTEM_STATUS,
        "pps": pps,
        "total_events": total_logs,
        "critical_count": critical_count,
        "warning_count": warning_count,
        "info_count": info_count,
        "avg_threat_score": avg_score,
        "high_risk_score": high_risk,
        "current_time": current_time,
        "last_profile": last_profile,
    }

@app.route('/')
def index():
    data = get_dashboard_data(limit=50)

    return render_template(
        'index.html',
        events=data["events"],
        system_status=data["system_status"],
        pps=data["pps"],
        total_events=data["total_events"],
        critical_count=data["critical_count"],
        warning_count=data["warning_count"],
        info_count=data["info_count"],
        avg_threat_score=data["avg_threat_score"],
        high_risk_score=data["high_risk_score"],
        current_time=data["current_time"],
        last_profile=data["last_profile"]
    )

@app.route('/api/dashboard')
def dashboard_api():
    data = get_dashboard_data(limit=50)
    return jsonify(data)

if __name__ == '__main__':
    # host='0.0.0.0' makes the dashboard accessible from Laptop B
    app.run(host='0.0.0.0', port=5000, debug=False)