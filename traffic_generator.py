import socket
import time
import sys

# ===========================================================
# CONFIGURATION: Replace this with Laptop A's actual IP address
# You can find Laptop A's IP by running 'ipconfig' on its terminal.
# ===========================================================
TARGET_IP = "192.168.X.X" 

def send_info_packet():
    """Simulates a standard connection (INFO Level)."""
    print(f"[+] Sending INFO: Normal TCP handshake to {TARGET_IP}:80...")
    try:
        # We try to connect to a standard web port (80)
        # This triggers the 'New Connection' logic in your monitor
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((TARGET_IP, 80)) 
        s.close()
    except Exception as e:
        print(f"    (Note: Handshake sent, though port 80 might be closed)")

def send_warning_packet():
    """Sends a packet larger than 1500 bytes (WARNING Level)."""
    print(f"[+] Sending WARNING: Large UDP packet (2000 bytes) to {TARGET_IP}...")
    # Creating a data string that exceeds the 1500 byte limit set in analyzer.py
    large_payload = b"A" * 2000 
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(large_payload, (TARGET_IP, 9999))
    sock.close()

def send_critical_packet():
    """Attempts to connect to a sensitive port (CRITICAL Level)."""
    print(f"[+] Sending CRITICAL: Attempting SSH access on port 22...")
    try:
        # Port 22 is for SSH. Your analyzer flags this as a potential threat.
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((TARGET_IP, 22))
        s.close()
    except Exception as e:
        print(f"    (Note: Port 22 probe sent to {TARGET_IP})")

def main_menu():
    if TARGET_IP == "192.168.X.X":
        print("!!! ERROR: You must edit the code and set TARGET_IP to Laptop A's IP address !!!")
        sys.exit()

    print("===============================================")
    print("   NEMS TRAFFIC GENERATOR (CLIENT SIDE)       ")
    print("===============================================")
    print(f"Targeting Monitor at: {TARGET_IP}")
    
    while True:
        print("\nWhat event would you like to simulate?")
        print("1. [INFO]     Standard Web Connection")
        print("2. [WARNING]  Large Data Transfer")
        print("3. [CRITICAL] Unauthorized Port Access (SSH)")
        print("4. [STORM]    Send multiple random events")
        print("5. Exit")
        
        choice = input("\nSelect an option (1-5): ")

        if choice == '1':
            send_info_packet()
        elif choice == '2':
            send_warning_packet()
        elif choice == '3':
            send_critical_packet()
        elif choice == '4':
            print("[!] Starting 5-second traffic storm...")
            for _ in range(3):
                send_info_packet()
                send_warning_packet()
                send_critical_packet()
                time.sleep(0.5)
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid selection. Try again.")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nStopped by user.")