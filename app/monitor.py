from scapy.all import sniff, IP, TCP, UDP, Raw, conf
from app.analyzer import analyze_packet
from app.utils import get_local_ip

def process_packet(packet):
    """dissects raw packets and passes them to the analyzer."""
    try:
        if packet.haslayer(IP):
            packet_info = {
                'src': packet[IP].src,
                'dst': packet[IP].dst,
                'size': len(packet),
                'port': None,
                'flags': "",
                'profile': None,
            }

            if packet.haslayer(TCP):
                packet_info['port'] = packet[TCP].dport
                packet_info['flags'] = str(packet[TCP].flags)
            elif packet.haslayer(UDP):
                packet_info['port'] = packet[UDP].dport
                packet_info['flags'] = "U"

            if packet.haslayer(Raw):
                raw_payload = bytes(packet[Raw].load)
                marker = b"NEMS_PROFILE="
                idx = raw_payload.find(marker)
                if idx != -1:
                    end = raw_payload.find(b";", idx)
                    if end != -1:
                        profile_bytes = raw_payload[idx + len(marker):end]
                        packet_info['profile'] = profile_bytes.decode("ascii", errors="ignore").upper()

            analyze_packet(packet_info)
    except Exception:
        pass

def start_sniffing():
    """Dynamically finds the correct network interface by IP."""
    target_ip = get_local_ip()
    selected_iface = None

    # Search all system interfaces for the one with your IP
    for iface_name in conf.ifaces:
        iface = conf.ifaces[iface_name]
        if iface.ip == target_ip:
            selected_iface = iface
            break

    print("=" * 50)
    if selected_iface:
        print(f"[*] NEMS Sniffer: Bound to {selected_iface.description}")
        print(f"[*] IP: {selected_iface.ip} | MAC: {selected_iface.mac}")
        # Pass the actual interface object instead of a string or index
        sniff(prn=process_packet, store=0, iface=selected_iface)
    else:
        print("[!] WARNING: Target IP not found on any interface.")
        print("[*] Falling back to default interface...")
        sniff(prn=process_packet, store=0)
    print("=" * 50)