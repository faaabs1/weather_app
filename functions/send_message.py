from dotenv import load_dotenv
import requests
import os

load_dotenv()
SLACK_WEBHOOK = os.getenv('SLACK_WEBHOOK')


def send_slack_message(text):
    """Sendet den fertigen Text an Slack."""
    if "https" not in SLACK_WEBHOOK:
        print("❌ Fehler: Keine gültige Slack-URL eingetragen.")
        return

    payload = {"text": text}
    
    try:
        response = requests.post(
            SLACK_WEBHOOK, 
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            print("✅ Nachricht erfolgreich an Slack gesendet!")
        else:
            print(f"⚠️ Fehler bei Slack: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"⚠️ Verbindungsfehler zu Slack: {e}")