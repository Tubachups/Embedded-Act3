from flask import Flask, Response
from camera import init_camera, cleanup_camera, get_camera
import io
import time
import atexit

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Register cleanup function
atexit.register(cleanup_camera)

@app.route('/')
def index():
    return '<h1>Pi Camera asdsad</h1><img src="/stream" width="640" height="480">'

@app.route('/stream')
def stream():
    init_camera()
    
    picam2 = get_camera()
    if picam2 is None:
        return "Camera not available", 503
    
    def generate():
        try:
            while True:
                stream = io.BytesIO()
                picam2.capture_file(stream, format='jpeg')
                stream.seek(0)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + 
                       stream.read() + b'\r\n')
                time.sleep(0.1)
        except Exception as e:
            print(f"Stream generation error: {e}")
    
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    finally:
        cleanup_camera()