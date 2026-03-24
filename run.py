import os
import sys
from app.database import init_db
from app.monitor import start_sniffing
from app.utils import log_event, get_local_ip

def setup_environment():
    """Ensures the necessary directories exist before starting."""
    if not os.path.exists('data'):
        os.makedirs('data')
        log_event("SUCCESS", "Created 'data' directory.")
    
    if not os.path.exists('logs'):
        os.makedirs('logs')
        log_event("SUCCESS", "Created 'logs' directory.")

def main():
    # 1. Print a cool header
    print("="*50)
    print("   NETWORK EVENT MONITORING SYSTEM (NEMS) v1.0   ")
    print("="*50)

    # 2. Setup folders and DB
    setup_environment()
    init_db()
    log_event("SUCCESS", "Database initialized.")

    # 3. Identify local machine info
    local_ip = get_local_ip()
    log_event("INFO", f"System running on Local IP: {local_ip}")

    # 4. Start the Sniffer
    try:
        log_event("INFO", "Starting packet capture... (Press Ctrl+C to stop)")
        start_sniffing()
    except PermissionError:
        log_event("CRITICAL", "Access Denied! Please run as Administrator/Sudo.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n")
        log_event("WARNING", "Shutdown signal received. Stopping NEMS...")
        sys.exit(0)

if __name__ == "__main__":
    main()