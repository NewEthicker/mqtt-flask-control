from flask import Flask, request, jsonify, render_template_string
import time

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>EC200U Live</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background:#0a0a1a; color:#00ff88; font-family:monospace; 
               text-align:center; padding:50px; }
        .counter { font-size:6em; border:2px solid #00ff88; 
                   border-radius:20px; padding:20px; display:inline-block; }
        .latency { font-size:1.5em; color:#ffaa00; margin:15px; }
    </style>
</head>
<body>
    <h1>⚡ EC200U LIVE</h1>
    <div class="counter" id="counter">--</div>
    <div class="latency" id="latency">Waiting...</div>
    <p id="time"></p>
</body>
<script>
    setInterval(async () => {
        try {
            const resp = await fetch('/api/data');
            const data = await resp.json();
            document.getElementById('counter').textContent = data.counter;
            document.getElementById('latency').textContent = data.latency + ' ms';
            document.getElementById('time').textContent = data.timestamp;
        } catch(e) {}
    }, 2000);
</script>
</html>
'''

latest = {"counter": 0, "latency": 0, "timestamp": ""}

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/api/data')
def get_data():
    return jsonify(latest)

@app.route('/counter', methods=['POST'])
def counter():
    server_time = time.time()
    data = request.get_json(force=True, silent=True) or {}
    device_time = data.get('time', server_time)
    counter_val = data.get('counter', 0)
    latency = int((server_time - device_time) * 1000) if device_time else 0
    
    latest['counter'] = counter_val
    latest['latency'] = latency
    latest['timestamp'] = time.strftime('%H:%M:%S')
    
    print(f"📥 Counter: {counter_val} | Latency: {latency}ms")
    
    return jsonify({"status": "ok", "server_time": server_time})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
