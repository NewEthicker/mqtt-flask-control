from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/counter', methods=['POST'])
def counter():
    data = request.get_json(force=True, silent=True) or {}
    counter_val = data.get('counter', 0)
    print(f"📥 Counter: {counter_val}")
    return jsonify({"status": "ok", "counter": counter_val})

@app.route('/')
def home():
    return jsonify({"status": "running"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
