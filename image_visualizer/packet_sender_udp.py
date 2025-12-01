import socket
import time
from PIL import Image

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
target = ("127.0.0.1", 9000)

# Load grayscale image
img = Image.open("test_image.png").convert("L")
width, height = img.size
img_bytes = img.tobytes()
total_bytes = width * height

packet_size = 1024  # bytes per packet
num_packets = (total_bytes + packet_size - 1) // packet_size

print(f"[UDP] Sending {num_packets} packets...")

for i in range(num_packets):
    start = i * packet_size
    end = start + packet_size
    payload = img_bytes[start:end]
    # Pad last payload if necessary
    if len(payload) < packet_size:
        payload += bytes(packet_size - len(payload))
    header = i.to_bytes(2, 'big') + b'\x00\x01' + len(payload).to_bytes(2, 'big')
    packet = header + payload
    sock.sendto(packet, target)
    time.sleep(0.01)

print("[UDP] Image sending complete")
