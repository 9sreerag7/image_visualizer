''' import cv2

def show_live_image(img):
    cv2.imshow("Live Image", img)
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        return False
    return True '''


'''import cv2

def show_live_image(img, wait_time=20000):
    """
    Displays the image.
    wait_time: milliseconds to wait before auto-close. If 0, waits until 'q' is pressed.
    Returns False if user presses 'q', else True.
    """
    cv2.imshow("Live Image", img)
    
    if wait_time > 0:
        cv2.waitKey(wait_time)
        cv2.destroyAllWindows()
        return True
    else:
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            cv2.destroyAllWindows()
            return False
        return True
'''




# live_viewer.py
import cv2

def show_live_image_opencv(img, window_name="Live Image"):
    """
    Show an image with a very short waitKey to keep window responsive.
    Use cv2.imshow + cv2.waitKey(1) to update live.
    """
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.imshow(window_name, img)
    # Small waitKey to allow GUI to update. Return key pressed if any.
    key = cv2.waitKey(1) & 0xFF
    return key

def close_live_viewer(window_name="Live Image"):
    cv2.destroyWindow(window_name)
