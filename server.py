import os
import json
from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)
GLOCKE_FILE = "glocke.json"

@app.route("/")
def home():
    return "Narions Glockensystem läuft."

@app.route("/mark-glocke", methods=["POST"])
def mark_glocke():
    now = datetime.now().isoformat()
    with open(GLOCKE_FILE, "w") as f:
        json.dump({"last_glocke": now}, f)
    return jsonify({"message": "🔔 Glocke markiert", "zeit": now})

@app.route("/status", methods=["GET"])
def status():
    if not os.path.exists(GLOCKE_FILE):
        return jsonify({"status": "❌ Keine Glocke gefunden"})
    with open(GLOCKE_FILE, "r") as f:
        data = json.load(f)
    return jsonify({"status": "✅ Letzte Glocke", "zeit": data.get("last_glocke")})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)