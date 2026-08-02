from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/counter', methods=['POST', 'GET'])
def counter():
    if request.method == 'POST':
        data = request.get_json(force=True, silent=True) or {}
        counter_val = data.get('counter', 0)
        print(f"📥 Counter: {counter_val}")
        return jsonify({"status": "ok", "counter": counter_val})
    else:
        return jsonify({"status": "ok", "message": "POST your counter here!"})

@app.route('/')
def home():
    return jsonify({
        "status": "running",
        "endpoints": {
            "/": "This page",
            "/counter": "POST JSON {\"counter\": 42}"
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
