import socket
import datetime
import os

class Colors:
    """ANSI color codes for pretty terminal output."""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def get_timestamp():
    """Returns the current time formatted for logs."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_local_ip():
    """Finds the IP address of the machine running this script."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # We 'connect' to a public DNS to see which interface the OS uses
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"

def resolve_hostname(ip):
    """Converts an IP address to a readable hostname."""
    try:
        hostname, _, _ = socket.gethostbyaddr(ip)
        return hostname
    except socket.herror:
        return "Unknown Host"

def log_event(level, message):
    """Prints a formatted, color-coded message to the terminal and a log file."""
    timestamp = get_timestamp()
    formatted_msg = f"[{timestamp}] [{level}] {message}"
    
    # 1. Print to Terminal with Colors
    color = Colors.OKCYAN
    if level == "CRITICAL": color = Colors.FAIL
    elif level == "WARNING": color = Colors.WARNING
    elif level == "SUCCESS": color = Colors.OKGREEN
    print(f"{color}{formatted_msg}{Colors.ENDC}")

    # 2. Write to the Log File (Only if the folder exists)
    if os.path.exists("logs"):
        log_path = os.path.join("logs", "network_events.log")
        with open(log_path, "a") as f:
            f.write(formatted_msg + "\n")