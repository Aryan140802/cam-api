from flask import Flask, render_template, Response, request, jsonify
from camera import camera_stream
import cv2
import os
import numpy as np

from datetime import datetime

app = Flask(__name__)

# Directory to save snapshots
SNAPSHOT_DIR = 'snapshots'

if not os.path.exists(SNAPSHOT_DIR):
    os.makedirs(SNAPSHOT_DIR)



@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen_frame():
    """Video streaming generator function."""
    while True:
        frame = camera_stream()
    
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concatenate frame one by one and show result


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    resp=Response(gen_frame(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/take_snapshot', methods=['POST'])
def take_snapshot(): 
    """Endpoint to take a snapshot from the video feed."""
    frame = camera_stream()
    frame = np.asarray(bytearray(frame), dtype="uint8")

    # Generate timestamp for filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    filename = os.path.join(SNAPSHOT_DIR, f'snapshot_{timestamp}.jpg')
    cv2.imwrite(filename, cv2.imdecode(frame, cv2.IMREAD_COLOR))

    return jsonify({'status': 'success', 'snapshot_path': filename})





if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
