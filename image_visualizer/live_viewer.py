''' import cv2

def show_live_image(img):
    cv2.imshow("Live Image", img)
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        return False
    return True '''


import cv2

def show_live_image(img, wait_time=5000):
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
