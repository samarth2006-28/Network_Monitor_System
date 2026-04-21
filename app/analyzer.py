import time
from collections import deque
from app.database import save_event
from app.utils import get_local_ip

# --- CONFIGURATION & STATE ---
MY_IP = get_local_ip()
SYSTEM_STATUS = "NORMAL"
IGNORE_SELF_TRAFFIC = False

# PHASE II: Congestion Window
# Deque allows for high-performance O(1) appends and pops
packet_timestamps = deque(maxlen=500)
PPS_THRESHOLD = 50.0  # Threshold for 'Congestion Resolution' mode

def check_congestion():
    """
    Calculates current Packets Per Second (PPS).
    Returns (bool: is_congested, float: current_pps)
    """
    now = time.time()
    packet_timestamps.append(now)
    
    # Need a minimum sample size for accuracy
    if len(packet_timestamps) < 20:
        return False, 0.0
        
    time_diff = now - packet_timestamps[0]
    if time_diff > 0:
        pps = len(packet_timestamps) / time_diff
        return pps > PPS_THRESHOLD, round(pps, 2)
    
    return False, 0.0

def calculate_threat_score(packet_data):
    """
    PHASE III: Heuristic Threat Scoring Algorithm.
    Generates a probability score between 0.0 and 1.0.
    """
    score = 0.0
    port = packet_data.get('port')
    size = packet_data.get('size', 0)
    flags = packet_data.get('flags')

    # Factor 1: Known Attack Vectors (Ports) - 50% Weight
    # SSH(22), Telnet(23), RDP(3389), SMB(445)
    if port in [22, 23, 3389, 445]:
        score += 0.50
    
    # Factor 2: Payload Anomaly (MTU Violations) - 30% Weight
    if size > 1500:
        score += 0.30
        
    # Factor 3: Protocol Intent (SYN/Handshake) - 20% Weight
    if flags == 'S':
        score += 0.20
        
    return round(min(score, 1.0), 2)

def analyze_packet(packet_data):
    """
    The Core Processing Engine. 
    Handles Filtering -> Congestion -> AI Scoring -> Resolution -> Logging.
    """
    global SYSTEM_STATUS
    
    src = packet_data.get('src')
    dst = packet_data.get('dst')
    port = packet_data.get('port')
    flags = packet_data.get('flags')
    size = packet_data.get('size', 0)
    profile = packet_data.get('profile')

    # --- STEP 1: LOCAL NOISE FILTERING ---
    if IGNORE_SELF_TRAFFIC and src == MY_IP:
        return

    # --- STEP 2: CONGESTION MONITORING (PHASE II) ---
    is_congested, current_pps = check_congestion()
    
    # Handle State Transitions
    if is_congested and SYSTEM_STATUS == "NORMAL":
        SYSTEM_STATUS = "CONGESTED"
        save_event("SYSTEM: STATUS CHANGE", "Monitor", "Local", 
                   f"High Traffic ({current_pps} PPS). Throttling mode active.", 0.1)
    
    elif not is_congested and SYSTEM_STATUS == "CONGESTED":
        SYSTEM_STATUS = "NORMAL"
        save_event("SYSTEM: STATUS CHANGE", "Monitor", "Local", 
                   f"Traffic stabilized ({current_pps} PPS). Normal mode active.", 0.0)

    # --- STEP 3: THREAT ANALYSIS (PHASE III) ---
    threat_score = calculate_threat_score(packet_data)

    # --- STEP 4: CONGESTION RESOLUTION (THROTTLING) ---
    # If congested, we drop packets with a threat probability < 70% 
    # to preserve system I/O and prevent database locking.
    if SYSTEM_STATUS == "CONGESTED" and threat_score < 0.7:
        return

    # --- STEP 5: EVENT CLASSIFICATION & PERSISTENCE ---
    # We assign types based on the final Threat Score
    event_type = "INFO: General Traffic"
    
    if threat_score >= 0.8:
        event_type = "CRITICAL: Security Intrusion"
    elif threat_score >= 0.5:
        event_type = "WARNING: Suspicious Activity"
    elif size > 1500:
        event_type = "WARNING: Large Data Burst"

    # Specific Detail Formatting
    if flags == 'S':
        details = f"Connection Handshake | Port: {port} | Score: {threat_score}"
    else:
        details = f"Packet size: {size} bytes | Port: {port} | Score: {threat_score}"

    if profile in {"INFO", "WARNING", "CRITICAL", "CONGESTION"}:
        details = f"[PROFILE:{profile}] {details}"

    # Always pass threat_score as the final parameter to match database.py
    save_event(event_type, src, dst, details, threat_score)