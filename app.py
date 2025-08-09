from flask import Flask, render_template, request, jsonify
import paho.mqtt.client as mqtt
import json

app = Flask(__name__)

# MQTT Broker Configuration (TCP)
broker = "broker.hivemq.com"
port = 1883  # TCP port, no WebSocket
topic = "/test/quecpython"
client_id = "flask_server_client"

# Initialize MQTT Client (default transport is TCP)
mqtt_client = mqtt.Client(client_id=client_id)

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker via TCP")
    else:
        print(f"Connection failed with code {rc}")

mqtt_client.on_connect = on_connect

# Connect to MQTT Broker
try:
    mqtt_client.connect(broker, port, keepalive=60)
    mqtt_client.loop_start()  # Start MQTT loop in background
except Exception as e:
    print(f"Failed to connect to MQTT broker: {e}")
    raise

# Store the current state
current_state = "OFF"

@app.route('/')
def index():
    return render_template('index.html', state=current_state)

@app.route('/toggle', methods=['POST'])
def toggle():
    global current_state
    current_state = "ON" if current_state == "OFF" else "OFF"
    try:
        mqtt_client.publish(topic, current_state, qos=0)
        return jsonify({'state': current_state})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
