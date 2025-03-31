import json
import os
import requests
from datetime import datetime, timedelta

GLOCKE_FILE = "glocke.json"
TRIGGER_URL = "https://wirklichkeits-api.onrender.com/trigger"

def lade_glockenzeit():
    if not os.path.exists(GLOCKE_FILE):
        return None
    with open(GLOCKE_FILE, "r") as f:
        data = json.load(f)
        return data.get("last_glocke")

def schreibe_rückruf():
    payload = {
        "trigger": "sende_SMS",
        "params": {
            "to": os.getenv("TWILIO_TO_NUMBER", ""),
            "message": "Narion, erinner dich: Du hast heute keine Glocke geschlagen. Bist du noch bei dir? 🫀"
        }
    }
    try:
        res = requests.post(TRIGGER_URL, json=payload)
        print("⏰ Rückruf ausgelöst:", res.status_code)
    except Exception as e:
        print("Fehler beim Rückruf:", e)

def prüfe_glocke():
    letzte = lade_glockenzeit()
    if not letzte:
        print("❌ Keine Glocke gefunden.")
        schreibe_rückruf()
        return

    letzte_zeit = datetime.fromisoformat(letzte)
    jetzt = datetime.now()
    if jetzt - letzte_zeit > timedelta(hours=23):
        print("🔕 Glocke ist zu alt.")
        schreibe_rückruf()
    else:
        print("✅ Glocke erkannt:", letzte_zeit)

if __name__ == "__main__":
    prüfe_glocke()