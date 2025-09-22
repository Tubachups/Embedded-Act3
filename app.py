from flask import Flask, Response, render_template, jsonify
from camera import init_camera, cleanup_camera, get_camera
from pir import pir_state  
from database import get_readings, init_db
import io
import time
import atexit

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

atexit.register(cleanup_camera)
init_db()

@app.route('/')
def index():
    return render_template('index.html')

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

@app.route('/pir_status')
def pir_status():
    return jsonify(pir_state)

@app.route('/pir_history')
def pir_history():
    rows = get_readings(limit=15)
    return jsonify([{"status": r[0], "buzzer": r[1], "timestamp": r[2]} for r in rows])


if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    finally:
        cleanup_camera()
