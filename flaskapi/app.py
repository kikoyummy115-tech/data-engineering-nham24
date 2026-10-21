# app.py
from flask import Flask, jsonify
import json
from pathlib import Path

app = Flask(__name__)

@app.route("/api/v1/customers", methods=["GET"])
def get_customers():
    file_path = Path("data.json")
    if not file_path.exists():
        return jsonify({"error": "data.json not found"}), 404
        
    with file_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return jsonify(data)

@app.route("/api/v2/customers", methods=["GET"])
def get_customers():
    file_path = Path("data.json")
    if not file_path.exists():
        return jsonify({"error": "data.json not found"}), 404
        
    with file_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return jsonify(data)

@app.route("/api/v3/customers", methods=["GET"])
def get_customers():
    file_path = Path("data.json")
    if not file_path.exists():
        return jsonify({"error": "data.json not found"}), 404
        
    with file_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return jsonify(data)

@app.route("/api/vn/customers", methods=["GET"])
def get_customers():
    file_path = Path("data.json")
    if not file_path.exists():
        return jsonify({"error": "data.json not found"}), 404
        
    with file_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return jsonify(data)


if __name__ == "__main__":
    app.run(port=5000, debug=True)