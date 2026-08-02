from flask import Flask, request, jsonify, render_template_string
import paho.mqtt.client as mqtt
import threading
import json
import time

app = Flask(__name__)

# Store latest data
latest = {"counter": 0, "latency_ms": 0, "timestamp": ""}

# MQTT Broker settings
MQTT_BROKER = "0.0.0.0"
MQTT_PORT = 1883

# HTML UI
HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>EC200U MQTT Live</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background:#0a0a1a; color:#00ff88; font-family:monospace; text-align:center; padding:30px; }
        .counter { font-size:5em; border:2px solid #00ff88; border-radius:20px; padding:20px; display:inline-block; margin:20px; }
        .latency { font-size:1.5em; color:#ffaa00; }
        .status { font-size:1em; color:#888; margin:10px; }
    </style>
</head>
<body>
    <h1>⚡ EC200U MQTT Live</h1>
    <div class="counter" id="counter">--</div>
    <div class="latency" id="latency">-- ms</div>
    <div class="status" id="time">--</div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/paho-mqtt/1.0.1/mqttws31.js"></script>
    <script>
        const client = new Paho.MQTT.Client(
            location.hostname === 'localhost' ? 'localhost' : location.hostname,
            9001,
            "web_" + Math.random().toString(16)
        );
        
        client.onMessageArrived = (msg) => {
            const data = JSON.parse(msg.payloadString);
            document.getElementById('counter').textContent = data.counter;
            document.getElementById('latency').textContent = data.latency_ms + ' ms';
            document.getElementById('time').textContent = data.timestamp;
        };
        
        client.connect({
            onSuccess: () => {
                client.subscribe("ec200u/data");
                document.getElementById('counter').textContent = 'Connected';
            }
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/api/latest')
def get_latest():
    return jsonify(latest)

@app.route('/counter', methods=['POST'])
def counter():
    data = request.get_json(force=True, silent=True) or {}
    server_time = time.time()
    device_time = data.get('time', server_time)
    latency = int((server_time - device_time) * 1000) if device_time else 0
    
    latest.update({
        "counter": data.get('counter', 0),
        "latency_ms": latency,
        "timestamp": time.strftime('%H:%M:%S')
    })
    
    return jsonify({"status": "ok"})

# MQTT Broker
def start_mqtt_broker():
    def on_connect(client, userdata, flags, rc):
        print(f"MQTT Broker: Client connected (rc={rc})")
    
    def on_message(client, userdata, msg):
        try:
            data = json.loads(msg.payload.decode())
            server_time = time.time()
            device_time = data.get('time', server_time)
            latency = int((server_time - device_time) * 1000) if device_time else 0
            
            latest.update({
                "counter": data.get('counter', 0),
                "latency_ms": latency,
                "timestamp": time.strftime('%H:%M:%S')
            })
            print(f"📥 MQTT Counter: {data.get('counter')} | Latency: {latency}ms")
        except Exception as e:
            print(f"MQTT Error: {e}")
    
    broker = mqtt.Client()
    broker.on_connect = on_connect
    broker.on_message = on_message
    broker.bind(MQTT_BROKER, MQTT_PORT)
    broker.listen_loop()

if __name__ == '__main__':
    threading.Thread(target=start_mqtt_broker, daemon=True).start()
    print("✅ Flask + MQTT Broker running on port 80")
    app.run(host='0.0.0.0', port=80)
