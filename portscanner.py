import socket
from concurrent.futures import ThreadPoolExecutor

PORT_SERVICES = {21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS", 80: "HTTP", 443: "HTTPS", 110: "POP3", 143: "IMAP", 3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL", 6379: "Redis", 8080: "HTTP Alt", 27017: "MongoDB"}
PORT_PROTOCOLS = {21: "TCP", 22: "TCP", 23: "TCP", 25: "TCP", 53: "UDP", 80: "TCP", 443: "TCP", 110: "TCP", 143: "TCP", 3306: "TCP", 3389: "TCP", 5432: "TCP", 6379: "TCP", 8080: "TCP", 27017: "TCP"}
PORT_VERSIONS = {21: "FTP Version: 2.0+", 22: "SSH Version: 2.0", 23: "Telnet Version: 1.0", 80: "HTTP Version: 1.1/2.0", 443: "HTTPS Version: 1.1/2.0", 3306: "MySQL Version: 5.7+", 5432: "PostgreSQL Version: 13+"}

def get_http_version(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)
            sock.connect((ip, port))
            sock.send(b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n")
            response = sock.recv(1024).decode()
            return "HTTP/2" if "HTTP/2" in response else "HTTP/1.1" if "HTTP/1.1" in response else "Unknown"
    except:
        return "Unknown"

def scan_port(ip, port, protocol):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM if protocol == "TCP" else socket.SOCK_DGRAM) as sock:
            sock.settimeout(0.05)
            if sock.connect_ex((ip, port)) == 0:
                service = PORT_SERVICES.get(port, "Unknown")
                version = get_http_version(ip, port) if port == 80 else PORT_VERSIONS.get(port, "Unknown")
                protocol_type = PORT_PROTOCOLS.get(port, "TCP")
                print(f"Port {port} open - Service: {service}, Protocol: {protocol_type}, Version: {version}")
                return (port, service, protocol_type, version)
    except:
        return None

def port_scan(ip, start_port, end_port):
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(scan_port, ip, port, PORT_PROTOCOLS.get(port, "TCP")) for port in range(start_port, end_port + 1)]
        return [future.result() for future in futures if future.result()]

if __name__ == "__main__":
    target_ip = input("IP address: ")
    start_port = int(input("Start port: "))
    end_port = int(input("End port: "))
    
    open_ports = port_scan(target_ip, start_port, end_port)
    print("\nScan Complete!")
    if open_ports:
        for port, service, protocol, version in open_ports:
            print(f"Port {port}: Service: {service}, Protocol: {protocol}, Version: {version}")
    else:
        print("No open ports found.")
