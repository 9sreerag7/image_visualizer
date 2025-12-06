'''import socket
import time
from PIL import Image

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
target = ("127.0.0.1", 9000)

# Load grayscale image
img = Image.open("test.png").convert("L")
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
'''






# packet_sender_udp.py
import socket
import time
from PIL import Image
import os

TARGET = ("127.0.0.1", 9000)
PACKET_PAYLOAD_SIZE = 4096   # payload bytes per UDP packet (tuneable)
SEND_DELAY = 0.001           # seconds between packets (tuneable)

def send_image(path):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # optional: increase send buffer if desired
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4 * 1024 * 1024)

    img = Image.open(path).convert("L")
    width, height = img.size
    img_bytes = img.tobytes()
    total_bytes = len(img_bytes)
    total_chunks = (total_bytes + PACKET_PAYLOAD_SIZE - 1) // PACKET_PAYLOAD_SIZE

    print(f"[SENDER] Image: {path} -> {width}x{height}, {total_bytes} bytes, {total_chunks} chunks")

    for chunk_index in range(total_chunks):
        start = chunk_index * PACKET_PAYLOAD_SIZE
        end = start + PACKET_PAYLOAD_SIZE
        payload = img_bytes[start:end]

        # CCSDS fake primary header (6 bytes)
        packet_id = (0x01).to_bytes(2, 'big')
        seq = (0x0001).to_bytes(2, 'big')
        pkt_len = (len(payload)).to_bytes(2, 'big')

        # Metadata (width, height, total_bytes, chunk_index, total_chunks)
        width_b = width.to_bytes(4, 'big')
        height_b = height.to_bytes(4, 'big')
        total_bytes_b = total_bytes.to_bytes(8, 'big')
        chunk_index_b = chunk_index.to_bytes(4, 'big')
        total_chunks_b = total_chunks.to_bytes(4, 'big')

        packet = packet_id + seq + pkt_len + width_b + height_b + total_bytes_b + chunk_index_b + total_chunks_b + payload
        sock.sendto(packet, TARGET)
        time.sleep(SEND_DELAY)

    print("[SENDER] Done sending.")

if __name__ == "__main__":
    # change filename to your path; put your test image in the same folder or give full path
    PATH = "test_image5.png"
    '''if not os.path.exists(PATH):
        # create a quick test image if missing (gradient)
        from PIL import ImageDraw
        print("[SENDER] test.png not found, creating a gradient test image (6000x4000). This will be large.")
        img = Image.new("L", (6000, 4000))
        draw = ImageDraw.Draw(img)
        for y in range(4000):
            # gradient row
            row = bytes( ( (x*y)//1000 % 256 for x in range(6000) ) )
            img.putdata(row, y*6000) if False else None
        # simpler: use numpy to generate and save
        import numpy as np
        arr = np.tile(np.arange(6000, dtype=np.uint8), (4000,1))
        img = Image.fromarray(arr)
        img.save(PATH)
        print("[SENDER] test.png created.")'''

    send_image(PATH)
