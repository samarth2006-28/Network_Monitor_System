from scapy.all import sniff, IP, TCP, UDP
from app.analyzer import analyze_packet

def packet_callback(packet):
    """
    Extracts core data from raw packets and passes it to the analyzer.
    """
    if packet.haslayer(IP):
        # Basic IP information
        packet_info = {
            'src': packet[IP].src,
            'dst': packet[IP].dst,
            'size': len(packet),
            'port': None,
            'flags': None
        }

        # Check for TCP specific data (like SYN/ACK flags)
        if packet.haslayer(TCP):
            packet_info['port'] = packet[TCP].dport
            packet_info['flags'] = packet[TCP].flags
        
        # Check for UDP specific data
        elif packet.haslayer(UDP):
            packet_info['port'] = packet[UDP].dport

        # Pass the extracted info to the Brain
        analyze_packet(packet_info)

def start_sniffing(interface=None):
    """
    Starts the Scapy sniffing process.
    'interface' can be 'Wi-Fi' or 'Ethernet'. If None, Scapy chooses default.
    """
    if interface:
        print(f"[*] NEMS Sniffer active on interface: {interface}")
    else:
        print("[*] NEMS Sniffer active on default network interface...")
    
    # store=0 tells Scapy not to keep packets in memory (prevents RAM crashes)
    sniff(iface=interface, prn=packet_callback, store=0)