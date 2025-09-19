from picamera2 import Picamera2

picam2 = None

def init_camera():
    global picam2
    try:
        if picam2 is None:
            picam2 = Picamera2()
            picam2.start()
    except Exception as e:
        print(f"Camera initialization error: {e}")
        picam2 = None

def get_camera():
    return picam2

def cleanup_camera():
    global picam2
    if picam2:
        try:
            picam2.stop()
            picam2.close()
        except:
            pass
        picam2 = None