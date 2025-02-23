from flask import Flask, request, jsonify

app = Flask(__name__)

requests_list = []

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    if 'youtube_url' in data:
        requests_list.append(data['youtube_url'])
        return jsonify({"message": "Link mentve!"}), 200
    return jsonify({"error": "Hibás kérés"}), 400

@app.route('/get_links', methods=['GET'])
def get_links():
    if requests_list:
        return jsonify({"youtube_url": requests_list.pop(0)})
    return jsonify({"youtube_url": None})
