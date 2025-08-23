from flask import Flask, Response, request, jsonify
import json
import threading
import time

# Import C++ module (will be built via pybind11)
try:
    import montecpp
except Exception:
    montecpp = None
import os
import subprocess

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
GENERATOR_BIN = os.path.join(ROOT, 'bin', 'generator.exe')

app = Flask(__name__)

worker = None
worker_lock = threading.Lock()

def event_stream(stop_event, batch_size=100):
    circle = 0
    total = 0
    while not stop_event.is_set():
        if montecpp:
            # call C++ function to generate a batch
            pts, c, t = montecpp.generate_batch(batch_size)
        elif os.path.exists(GENERATOR_BIN):
            # call the CLI generator; it will print JSON to stdout
            try:
                proc = subprocess.run([GENERATOR_BIN, str(batch_size)], capture_output=True, text=True, check=True)
                j = json.loads(proc.stdout)
                pts = j.get('points', [])
                c = j.get('circle', 0)
                t = j.get('total', batch_size)
            except Exception:
                pts = []
                c = 0
                t = 0
        else:
            # fallback: generate random points in python
            import random
            pts = []
            c = 0
            for _ in range(batch_size):
                x = random.uniform(-1, 1)
                y = random.uniform(-1, 1)
                pts.append([x, y])
                if x*x + y*y <= 1.0:
                    c += 1
            t = batch_size

        circle += c
        total += t
        pi_est = 4.0 * circle / total if total > 0 else 0.0
        tau_est = 2.0 * pi_est
        payload = {
            'points': pts,
            'circle': circle,
            'total': total,
            'pi': pi_est,
            'tau': tau_est
        }
        yield f"data: {json.dumps(payload)}\n\n"
        time.sleep(0.05)

@app.route('/start', methods=['POST'])
def start():
    global worker
    if worker and worker['thread'].is_alive():
        return jsonify({'status': 'already running'})
    stop_event = threading.Event()
    t = threading.Thread(target=lambda: None, daemon=True)
    worker = {'thread': t, 'stop': stop_event}
    return jsonify({'status': 'started'})

@app.route('/stop', methods=['POST'])
def stop():
    global worker
    if not worker:
        return jsonify({'status': 'not running'})
    worker['stop'].set()
    worker = None
    return jsonify({'status': 'stopped'})

@app.route('/stream')
def stream():
    # Server-Sent Events streaming endpoint
    stop_event = threading.Event()
    return Response(event_stream(stop_event), mimetype='text/event-stream')

@app.route('/')
def index():
    return "Monte Carlo Tau API"

if __name__ == '__main__':
    app.run(port=5000, debug=True)
