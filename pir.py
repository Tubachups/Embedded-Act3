from gpiozero import MotionSensor, Buzzer
from datetime import datetime
from database import insert_reading
from camera import get_camera, capture_image, capture_video, is_camera_recording
from email_notif import send_email_notification
import threading
import time
import os

motion_sensor = MotionSensor(14)
buzzer = Buzzer(26)
pir_state = {
    "status": "Monitoring...",
    "buzzer": "OFF", 
    "last_capture": None, 
    "recording": False
    }

# Ensure directories exist
os.makedirs("static/motion_images", exist_ok=True)
os.makedirs("static/motion_videos", exist_ok=True)

def monitor_pir():
    global pir_state
    last_capture = 0
    last_motion_state = False  
    while True:
        if motion_sensor.motion_detected:
            if not last_motion_state:  
                pir_state["status"] = "Somebody here!"
                buzzer.on()
                pir_state["buzzer"] = "ON"
                insert_reading(pir_state["status"], pir_state["buzzer"])
                print("[PIR] Motion detected - DB insert")
                last_motion_state = True  

            # Limit captures to avoid spam (wait 6 seconds between captures)
            current_time = time.time()
            if current_time - last_capture > 6:
                picam2 = get_camera()
                if picam2 and not is_camera_recording():
                    try:
                        timestamp = datetime.now().strftime('%m-%d-%Y-%H-%M-%S')
                        img_file = f"static/motion_images/motion_{timestamp}.jpg"
                        video_file = f"static/motion_videos/motion_{timestamp}.h264"

                        # Capture image
                        capture_image(img_file)

                        # Send email notification with image
                        threading.Thread(target=send_email_notification, args=(img_file,), daemon=True).start()

                        # Then start video recording
                        pir_state["recording"] = True
                        capture_video(duration=5, output_path=video_file)
                        pir_state["last_capture"] = f"Image & Video: {timestamp}"

                        # Reset recording status after video completes
                        def reset_recording_status():
                            time.sleep(5.5)
                            pir_state["recording"] = False
                        threading.Thread(target=reset_recording_status, daemon=True).start()

                        print(f"[PIR] Motion detected - Image and video capture initiated")

                    except Exception as e:
                        print(f"[PIR] Error during capture: {e}")
                        pir_state["recording"] = False

                last_capture = current_time

        else:
            pir_state["status"] = "Monitoring..."
            buzzer.off()
            pir_state["buzzer"] = "OFF"
            last_motion_state = False  
        time.sleep(0.2)

# Start background monitoring thread
pir_thread = threading.Thread(target=monitor_pir, daemon=True)
pir_thread.start()