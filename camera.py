from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput
import time
import os
import threading
from datetime import datetime

picam2 = None
encoder = None
recording_lock = threading.Lock()
is_recording = False

def init_camera():
    global picam2, encoder
    try:
        if picam2 is None:
            picam2 = Picamera2()
            # Configure for video recording
            video_config = picam2.create_video_configuration(
                main={"size": (800, 600)},
                encode="main"
            )
            picam2.configure(video_config)
            encoder = H264Encoder(bitrate=10000000)
            picam2.start()
            print("[Camera] Initialized successfully")
    except Exception as e:
        print(f"Camera initialization error: {e}")
        picam2 = None

def get_camera():
    
    return picam2

def capture_video(duration=5, output_path=None):
    global picam2, encoder, is_recording
    
    if picam2 is None:
        print("[Camera] Not initialized")
        return None
    
    with recording_lock:
        if is_recording:
            print("[Camera] Already recording")
            return None
        is_recording = True
    
    try:
        # Generate filename if not provided
        if output_path is None:
            timestamp = datetime.now().strftime('%m-%d-%Y-%H-%M-%S')
            output_path = f"static/motion_videos/video_{timestamp}.h264"
            os.makedirs("static/motion_videos", exist_ok=True)
        
        # Start recording in a separate thread
        def record():
            try:
                print(f"[Camera] Starting {duration}s video recording: {output_path}")
                picam2.start_encoder(encoder, output=FileOutput(output_path))
                time.sleep(duration)
                picam2.stop_encoder()
                print(f"[Camera] Video saved: {output_path}")
            except Exception as e:
                print(f"[Camera] Recording error: {e}")
            finally:
                global is_recording
                is_recording = False
        
        # Start recording thread
        record_thread = threading.Thread(target=record, daemon=True)
        record_thread.start()
        
        return output_path
        
    except Exception as e:
        print(f"[Camera] Video capture error: {e}")
        is_recording = False
        return None

def capture_image(output_path=None):
    global picam2
    
    if picam2 is None:
        print("[Camera] Not initialized")
        return None
    
    try:
        if output_path is None:
            timestamp = datetime.now().strftime('%m-%d-%Y-%H-%M-%S')
            output_path = f"static/motion_images/image_{timestamp}.jpg"
            os.makedirs("static/motion_images", exist_ok=True)
        
        picam2.capture_file(output_path)
        print(f"[Camera] Image saved: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"[Camera] Image capture error: {e}")
        return None

def is_camera_recording():
    return is_recording

def cleanup_camera():
    global picam2, encoder
    if picam2:
        try:
            if is_recording:
                picam2.stop_encoder()
            picam2.stop()
            picam2.close()
            print("[Camera] Cleaned up")
        except Exception as e:
            print(f"[Camera] Cleanup error: {e}")
        picam2 = None
        encoder = None