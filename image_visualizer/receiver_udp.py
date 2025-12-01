''' import socket

def start_udp_receiver(port=9000):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", port))
    print(f"[UDP] Listening on port {port}...")

    while True:
        data, addr = sock.recvfrom(4096)
        yield data '''



import socket

def start_udp_receiver(port=9000):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", port))
    sock.settimeout(1)  # 1 seconds timeout
    print(f"[UDP] Listening on port {port}...")

    while True:
        try:
            data, addr = sock.recvfrom(4096)
            yield data
        except socket.timeout:
            continue  # loop again, allows Ctrl+C to work

