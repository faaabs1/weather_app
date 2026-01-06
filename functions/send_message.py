from dotenv import load_dotenv
import requests
import os

load_dotenv()
SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL')


def send_slack_message(text):
    """Sendet den fertigen Text an Slack."""
    if "https" not in SLACK_WEBHOOK_URL:
        print("❌ Fehler: Keine gültige Slack-URL eingetragen.")
        return

    payload = {"text": text}
    
    try:
        response = requests.post(
            SLACK_WEBHOOK_URL, 
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            print("✅ Nachricht erfolgreich an Slack gesendet!")
        else:
            print(f"⚠️ Fehler bei Slack: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"⚠️ Verbindungsfehler zu Slack: {e}")