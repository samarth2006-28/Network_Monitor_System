import time
from scapy.all import IP, TCP, Raw, send

# CONFIGURATION: Change this to Laptop A's IP address
TARGET_IP = "192.168.0.163"

def send_test_packet(port=80, size=64, label="INFO", flags="S"):
    print(f"[*] Sending {label} packet to port {port} (Size: {size} bytes, Flags: {flags})...")
    pkt = IP(dst=TARGET_IP) / TCP(dport=port, flags=flags) / Raw(load="X" * size)
    send(pkt, verbose=False)

def build_payload(profile_tag, size):
    """Build deterministic payload with a profile marker for dashboard detection."""
    marker = f"NEMS_PROFILE={profile_tag};"
    if size <= len(marker):
        return marker[:size]
    return marker + ("X" * (size - len(marker)))

def run_profile(name, packets, port, size, flags, delay, profile_tag):
    print(f"[>] Running {name}: {packets} packets | port={port} | size={size} | flags={flags}")
    payload = build_payload(profile_tag, size)
    for _ in range(packets):
        pkt = IP(dst=TARGET_IP) / TCP(dport=port, flags=flags) / Raw(load=payload)
        send(pkt, verbose=False)
        if delay > 0:
            time.sleep(delay)

def run_congestion_storm():
    print("[!] TRIGGERING THE STORM: Sending 260 packets rapidly...")
    payload = build_payload("CONGESTION", 80)
    for _ in range(260):
        pkt = IP(dst=TARGET_IP) / TCP(dport=80, flags="S") / Raw(load=payload)
        send(pkt, verbose=False)

if __name__ == "__main__":
    custom_target = input(f"Target IP [{TARGET_IP}]: ").strip()
    if custom_target:
        TARGET_IP = custom_target

    print("--- NEMS Traffic Generator & Testing Suite ---")
    print(f"[*] Active target: {TARGET_IP}")
    while True:
        print("\n1. Test INFO (Normal Traffic)")
        print("2. Test WARNING (Large Packet > 1500 bytes)")
        print("3. Test CRITICAL (Probe Port 22 - SSH)")
        print("4. Test CONGESTION (The Storm Mode)")
        print("5. Exit")
        
        choice = input("\nSelect a test case: ")
        
        if choice == '1':
            # INFO: Low-risk traffic (ACK, normal size) -> should stay clearly INFO.
            run_profile(
                name="INFO Baseline",
                packets=10,
                port=80,
                size=100,
                flags="A",
                delay=0.08,
                profile_tag="INFO",
            )
        elif choice == '2':
            # WARNING: Medium-risk traffic (SYN + large packet) -> warning-heavy entries.
            run_profile(
                name="WARNING Burst",
                packets=14,
                port=443,
                size=2200,
                flags="S",
                delay=0.05,
                profile_tag="WARNING",
            )
        elif choice == '3':
            # CRITICAL: High-risk (attack port + SYN + oversized payload) -> strong red signals.
            run_profile(
                name="CRITICAL Probe",
                packets=16,
                port=22,
                size=2200,
                flags="S",
                delay=0.04,
                profile_tag="CRITICAL",
            )
        elif choice == '4':
            run_congestion_storm()
        elif choice == '5':
            break
        else:
            print("Invalid choice.")