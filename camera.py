from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
import time
import os
import threading

picam2 = None
encoder = None

def init_camera():
    global picam2, encoder
    try:
        if picam2 is None:
            picam2 = Picamera2()
            encoder = H264Encoder()
            picam2.start()
    except Exception as e:
        print(f"Camera initialization error: {e}")
        picam2 = None

def get_camera():
    return picam2

def capture_motion_image():
    if picam2:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        image_path = f"static/motion_images/motion_{timestamp}.jpg"
        try:
            picam2.capture_file(image_path)
            return image_path
        except Exception as e:
            print(f"Image capture error: {e}")
    return None

def record_motion_video():
    if picam2:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        video_path = f"static/motion_images/motion_{timestamp}.h264"
        try:
            picam2.start_recording(encoder, video_path)
            time.sleep(3)  # Record for 3 seconds
            picam2.stop_recording()
            return video_path
        except Exception as e:
            print(f"Video recording error: {e}")
    return None

def cleanup_camera():
    global picam2
    if picam2:
        try:
            picam2.stop()
            picam2.close()
        except:
            pass
        picam2 = None