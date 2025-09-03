from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
from datetime import datetime, timezone

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
DATA_FILE = 'data.json'
PORT = 8000

# Default data structure
DEFAULT_DATA = {
    "people": [
        {"id": 1, "name": "Deniz", "status": "available", "lastUpdated": datetime.now().isoformat()},
        {"id": 2, "name": "Ecem", "status": "available", "lastUpdated": datetime.now().isoformat()},
        {"id": 3, "name": "Josh", "status": "available", "lastUpdated": datetime.now().isoformat()},
        {"id": 4, "name": "Lauren", "status": "available", "lastUpdated": datetime.now().isoformat()},
        {"id": 5, "name": "Noah", "status": "available", "lastUpdated": datetime.now().isoformat()},
        {"id": 6, "name": "River", "status": "available", "lastUpdated": datetime.now().isoformat()},
        {"id": 7, "name": "Sarah", "status": "available", "lastUpdated": datetime.now().isoformat()}
    ],
    "lastSync": datetime.now(timezone.utc).isoformat()
}

def initialize_data_file():
    if not os.path.exists(DATA_FILE):
        save_data(DEFAULT_DATA)

def load_data():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return DEFAULT_DATA

def save_data(data):
    try:
        data['lastSync'] = datetime.now(timezone.utc).isoformat()
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except:
        return False

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(load_data())

@app.route('/api/data', methods=['POST'])
def save_data_endpoint():
    new_data = request.get_json()
    if not new_data or 'people' not in new_data:
        return jsonify({"error": "Invalid data structure"}), 400
    return jsonify({"success": True}) if save_data(new_data) else (jsonify({"error": "Save failed"}), 500)

@app.route('/api/update-status', methods=['POST'])
def update_status():
    data = request.get_json()
    user_id = data.get('userId')
    status = data.get('status')
    if not user_id or not status:
        return jsonify({"error": "Missing fields"}), 400
    people_data = load_data()
    person = next((p for p in people_data['people'] if p['id'] == user_id), None)
    if not person:
        return jsonify({"error": "Person not found"}), 404
    person['status'] = status
    person['lastUpdated'] = datetime.now(timezone.utc).isoformat()
    return jsonify({"success": True, "person": person}) if save_data(people_data) else (jsonify({"error": "Save failed"}), 500)

@app.route('/api/upload-image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    user_id = request.form.get('userId')
    if not file or file.filename == '' or not user_id:
        return jsonify({'error': 'Missing file or userId'}), 400
    upload_path = os.path.join('static', 'uploads')
    os.makedirs(upload_path, exist_ok=True)
    filename = f"user_{user_id}.gif"
    filepath = os.path.join(upload_path, filename)
    file.save(filepath)
    data = load_data()
    for person in data['people']:
        if str(person['id']) == str(user_id):
            person['gif'] = f"/static/uploads/{filename}"
            break
    save_data(data)
    return jsonify({'success': True, 'url': f"/static/uploads/{filename}"})

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "data_file_exists": os.path.exists(DATA_FILE)
    })

if __name__ == '__main__':
    initialize_data_file()
    app.run(host='0.0.0.0', port=PORT, debug=False)
