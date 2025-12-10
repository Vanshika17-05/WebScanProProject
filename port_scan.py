import socket
import concurrent.futures

def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        sock.close()
        if result == 0:
            return port
    except:
        pass
    return None

def run_port_scan(target_domain):
    # Remove http:// to get just the domain/IP
    target_ip = target_domain.replace("http://", "").replace("https://", "").split("/")[0].split(":")[0]
    
    open_ports = []
    # Scan common ports: FTP, SSH, Telnet, SMTP, DNS, HTTP, POP3, HTTPS, MySQL
    common_ports = [21, 22, 23, 25, 53, 80, 110, 443, 3306, 8080, 8084]
    
    print(f"📡 Scanning ports on {target_ip}...")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_port = {executor.submit(scan_port, target_ip, port): port for port in common_ports}
        for future in concurrent.futures.as_completed(future_to_port):
            port = future.result()
            if port:
                open_ports.append(port)
                
    return open_ports, target_ip