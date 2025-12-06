''' import socket

def start_udp_receiver(port=9000):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", port))
    print(f"[UDP] Listening on port {port}...")

    while True:
        data, addr = sock.recvfrom(4096)
        yield data '''



'''import socket

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

'''



# receiver_udp.py
import socket

def start_udp_receiver(port=9000, recv_bufsize=4 * 1024 * 1024, timeout=1.0):
    """
    Generator yielding raw UDP packets (bytes).
    recv_bufsize: sets SO_RCVBUF to help with bursty traffic
    timeout: socket timeout (seconds) so Ctrl+C works
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", port))
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, recv_bufsize)
    sock.settimeout(timeout)
    print(f"[UDP] Listening on port {port} (recv_buf={recv_bufsize})...")

    while True:
        try:
            data, addr = sock.recvfrom(65536)  # receive up to 64KB per datagram
            yield data
        except socket.timeout:
            continue
        except GeneratorExit:
            break
        except KeyboardInterrupt:
            break
