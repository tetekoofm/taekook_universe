from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "pong"})

@app.route("/echo", methods=["POST"])
def echo():
    print("Raw data:", request.data)
    try:
        data = request.get_json(force=True)
        print("Parsed JSON:", data)
        return jsonify({"received": data})
    except Exception as e:
        print("Error parsing JSON:", e)
        return jsonify({"error": str(e)}), 400

@app.route('/submit_score', methods=['POST'])
def submit_score():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON received"}), 400

    print("Received JSON:", data)
    return jsonify({"success": True, "data": data})
    
if __name__ == "__main__":
    app.run(port=8888, debug=True)