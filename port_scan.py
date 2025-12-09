
import socket

def scan_ports(target):
    open_ports = []
    # Standard ports to check (Web, Mail, SSH, DNS)
    ports_to_check = [21, 22, 23, 25, 53, 80, 110, 443, 3306, 8080]
    
    # Remove "http://" if present for socket connection
    target = target.replace("http://", "").replace("https://", "").split("/")[0]

    for port in ports_to_check:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5) # Fast timeout to keep dashboard responsive
        result = sock.connect_ex((target, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    
    return open_ports