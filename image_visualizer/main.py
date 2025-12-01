''' from receiver_udp import start_udp_receiver
from ccsds_header_parser import parse_ccsds_header
from image_reconstructor import ImageReconstructor
from live_viewer import show_live_image

# Set width & height to match your test image
recon = ImageReconstructor(width=225, height=225)

try:
    for packet in start_udp_receiver(9000):
        parsed = parse_ccsds_header(packet)
        if parsed is None:
            continue
        recon.add_data(parsed["payload"])
        img = recon.get_image()
        if img is not None:
            if not show_live_image(img):
                break
            recon.reset()  # Clear buffer after showing full image
except KeyboardInterrupt:
    print("\n[UDP] Receiver stopped by user") '''


from receiver_udp import start_udp_receiver
from ccsds_header_parser import parse_ccsds_header
from image_reconstructor import ImageReconstructor
from live_viewer import show_live_image

recon = ImageReconstructor(width=225, height=225)

try:
    for packet in start_udp_receiver(9000):
        parsed = parse_ccsds_header(packet)
        if parsed is None:
            continue
        recon.add_data(parsed["payload"])
        img = recon.get_image()
        if img is not None:
            # Show the reconstructed image for 5 seconds
            show_live_image(img, wait_time=5000)
            recon.reset()  # Clear buffer for next image
except KeyboardInterrupt:
    print("\n[UDP] Receiver stopped by user")

