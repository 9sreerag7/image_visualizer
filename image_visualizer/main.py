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
import os

bytes_received = 0
rate_start_time = time.time()
frame_start_time = time.time()
total_bytes_frame = 0



# Nominal chunk size the sender will use (must match sender's packet_payload_size)
CHUNK_SIZE = 4096

recon = ImageReconstructor()
frame_count = 0
last_display_time = 0.0
DISPLAY_INTERVAL = 0.25  # seconds between GUI updates (avoid updating too frequently)

print("[MAIN] Starting receiver. Make sure you run sender AFTER receiver.")

try:
    for packet in start_udp_receiver(port=9000, recv_bufsize=8*1024*1024, timeout=1.0):
        bytes_received += len(packet)
        total_bytes_frame += len(packet)
        parsed = parse_ccsds_header(packet)
        if parsed is None:
            continue

        width = parsed["width"]
        height = parsed["height"]
        total_bytes = parsed["total_bytes"]
        chunk_index = parsed["chunk_index"]
        total_chunks = parsed["total_chunks"]
        payload = parsed["payload"]

        #print("[DEBUG] RECEIVER HEADER:", width, height, total_bytes)

        # Initialize reconstructor on first valid packet OR if image resolution changed
        if recon.buffer is None:
            print(f"[MAIN] Initializing reconstructor: {width}x{height}")
            recon.setup(width, height, total_bytes, total_chunks, CHUNK_SIZE)

        '''if (recon.buffer is None) or (recon.width != width or recon.height != height):
            print(f"[MAIN] Initializing reconstructor: {width}x{height}, total_bytes={total_bytes}, total_chunks={total_chunks}")
            recon.setup(width, height, total_bytes, total_chunks, CHUNK_SIZE)'''

        # Add chunk
        recon.add_chunk(chunk_index, payload)

        # Show progress occasionally (not every packet)
        prog = recon.progress() * 100
        if int(prog) % 10 == 0:  # print every ~5% change (approx)
            print(f"[MAIN] Progress: {len(recon.received_chunks)}/{recon.total_chunks} chunks ({prog:.2f}%)", end='\r')

        if time.time() - rate_start_time >= 1.0:
            kbps = (bytes_received * 8) / 1000
            #print(f"[STATS] Data rate: {kbps:.2f} kbps", end=" | ")
            print(f"\n[STATS] Data rate: {kbps:.2f} kbps")
            bytes_received = 0
            rate_start_time = time.time()

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
            print("\n[MAIN] Image complete.")

            frame_count += 1
            frame_time = time.time() - frame_start_time
            avg_kbps = (total_bytes_frame * 8) / (frame_time * 1000)

            missing = recon.missing_chunks()

            print("\n===== FRAME STATISTICS =====")
            print(f"Frame number      : {frame_count}")
            print(f"Image resolution  : {recon.width} x {recon.height}")
            print(f"Total packets     : {recon.total_chunks}")
            print(f"Received packets  : {len(recon.received_chunks)}")
            print(f"Missing packets   : {len(missing)}")
            print(f"Average data rate : {avg_kbps:.2f} kbps")
            print("============================\n")


            final_img = recon.get_image()
            '''if final_img is not None:
                filename = f"frame_{frame_count}_{recon.width}x{recon.height}.png"
                cv2.imwrite(filename, final_img)'''
            
            output_dir = "output"
            os.makedirs(output_dir, exist_ok=True)
            filename = os.path.join(
                output_dir,
                f"frame_{frame_count}_{recon.width}x{recon.height}.png"
            )
            cv2.imwrite(filename, final_img)
            print(f"[MAIN] Saved full-resolution image as {filename}")

            '''missing = recon.missing_chunks()
            print(f"[STATS] Missing packets: {len(missing)}")'''

            # optional: still show scaled preview for 2 seconds
            cv2.imshow("Live Image", final_img)
            cv2.waitKey(5000)
            cv2.destroyAllWindows()

            recon.reset()
            frame_start_time = time.time()
            total_bytes_frame = 0
            last_display_time = 0.0
           



except KeyboardInterrupt:
    print("\n[MAIN] Receiver stopped by user.")
finally:
    try:
        close_live_viewer()
    except Exception:
        pass






