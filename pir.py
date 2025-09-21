from gpiozero import MotionSensor
import threading
import time
from camera import capture_motion_image, record_motion_video
import os

motion_sensor = MotionSensor(14)
pir_state = {"status": "Monitoring...", "last_detection": None}

# Ensure the motion_images directory exists
os.makedirs("static/motion_images", exist_ok=True)

def monitor_pir():
    global pir_state
    last_trigger_time = 0
    cooldown_period = 10  # Seconds between triggers

    while True:
        current_time = time.time()
        if motion_sensor.motion_detected:
            if current_time - last_trigger_time >= cooldown_period:
                pir_state["status"] = "Somebody here!"
                pir_state["last_detection"] = time.strftime("%Y-%m-%d %H:%M:%S")
                
                # Capture image and video
                image_path = capture_motion_image()
                video_path = record_motion_video()
                
                if image_path:
                    print(f"Motion detected! Image saved to: {image_path}")
                if video_path:
                    print(f"Motion video saved to: {video_path}")
                
                last_trigger_time = current_time
        else:
            pir_state["status"] = "Monitoring..."
        time.sleep(0.5)

# Start background monitoring thread
pir_thread = threading.Thread(target=monitor_pir, daemon=True)
pir_thread.start()