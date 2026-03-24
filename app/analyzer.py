from app.database import save_event
from app.utils import get_local_ip

# Identify this laptop's IP so we can filter it out
MY_IP = get_local_ip()

def analyze_packet(packet_data):
    """
    Decides if a packet is an 'Event'.
    Ignores traffic sent FROM this laptop to keep the logs clean.
    """
    src = packet_data.get('src')
    dst = packet_data.get('dst')
    port = packet_data.get('port')
    flags = packet_data.get('flags')
    size = packet_data.get('size', 0)

    # --- CHANGE FOR 2-DEVICE SETUP ---
    # We skip any packet where the source is this monitor laptop.
    # This prevents the monitor from 'logging itself'.
    if src == MY_IP:
        return

    # 1. Security Alert: Sensitive Port Access
    # Port 22 (SSH), 23 (Telnet), 3389 (Remote Desktop), 445 (SMB)
    critical_ports = [22, 23, 3389, 445]
    if port in critical_ports:
        event_type = "CRITICAL: Unauthorized Port Access"
        details = f"External device {src} attempted connection to sensitive port: {port}"
        save_event(event_type, src, dst, details)
        return # Skip further analysis for this packet

    # 2. Performance Alert: Large Packet (Potential Data Transfer)
    if size > 1500:
        event_type = "WARNING: Large Packet Detected"
        details = f"Large data transfer of {size} bytes detected from {src}"
        save_event(event_type, src, dst, details)

    # 3. Connection Info: New TCP Handshake
    # 'S' flag = SYN packet (the start of a connection)
    if flags == 'S':
        event_type = "INFO: New Connection Attempt"
        details = f"Device {src} is initiating a TCP handshake on port {port}"
        save_event(event_type, src, dst, details)