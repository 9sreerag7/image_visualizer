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


'''from receiver_udp import start_udp_receiver
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

'''






# main.py
import time
from receiver_udp import start_udp_receiver
from ccsds_header_parser import parse_ccsds_header
from image_reconstructor import ImageReconstructor
from live_viewer import show_live_image_opencv, close_live_viewer
import cv2

# Nominal chunk size the sender will use (must match sender's packet_payload_size)
CHUNK_SIZE = 4096

recon = ImageReconstructor()
last_display_time = 0.0
DISPLAY_INTERVAL = 0.25  # seconds between GUI updates (avoid updating too frequently)

print("[MAIN] Starting receiver. Make sure you run sender AFTER receiver.")

try:
    for packet in start_udp_receiver(port=9000, recv_bufsize=8*1024*1024, timeout=1.0):
        parsed = parse_ccsds_header(packet)
        if parsed is None:
            continue

        width = parsed["width"]
        height = parsed["height"]
        total_bytes = parsed["total_bytes"]
        chunk_index = parsed["chunk_index"]
        total_chunks = parsed["total_chunks"]
        payload = parsed["payload"]

        # Initialize reconstructor on first valid packet OR if image resolution changed
        if (recon.buffer is None) or (recon.width != width or recon.height != height):
            print(f"[MAIN] Initializing reconstructor: {width}x{height}, total_bytes={total_bytes}, total_chunks={total_chunks}")
            recon.setup(width, height, total_bytes, total_chunks, CHUNK_SIZE)

        # Add chunk
        recon.add_chunk(chunk_index, payload)

        # Show progress occasionally (not every packet)
        prog = recon.progress() * 100
        if int(prog) % 5 == 0:  # print every ~5% change (approx)
            print(f"[MAIN] Progress: {len(recon.received_chunks)}/{recon.total_chunks} chunks ({prog:.2f}%)", end='\r')

        # Live display throttle
        now = time.time()
        if now - last_display_time >= DISPLAY_INTERVAL:
            img = recon.get_image()
            # even if not complete, get_image returns array view (zeros in missing regions)
            if img is not None:
                key = show_live_image_opencv(img)
            else:
                # create temporary partial view from buffer (zeros show gaps)
                partial = recon.get_image()  # might be None until width/height set
                if partial is not None:
                    key = show_live_image_opencv(partial)
            last_display_time = now

            # If user presses 'q' in the CV window, exit
            if key == ord('q'):
                print("\n[MAIN] User requested exit (q).")
                break

        # If reconstruction complete, show final image & clean up for next frame
        if recon.is_complete():
            print("\n[MAIN] Image complete. Displaying final image...")
            final_img = recon.get_image()
            if final_img is not None:
                # show final for 3 seconds
                cv2.imshow("Live Image", final_img)
                cv2.waitKey(5000)
                cv2.destroyAllWindows()
            # reset for next image
            recon.reset()
            last_display_time = 0.0
except KeyboardInterrupt:
    print("\n[MAIN] Receiver stopped by user.")
finally:
    try:
        close_live_viewer()
    except Exception:
        pass






