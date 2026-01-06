from functions.llm_response import generate_ai_message
from functions.api_request import get_forecast, parse_weather_data
from functions.send_message import send_slack_message

LAT = 48.2082
LON = 16.3738


def main(lat,lon):
    # Schritt 1: Wetterdaten abrufen
    weather_data = get_forecast(lat, lon)
    
    # Schritt 2: Wetterdaten formatieren
    weather_data_string = parse_weather_data(weather_data)
    
    # Schritt 3: KI-Nachricht generieren
    ai_message = generate_ai_message(weather_data_string)
    
    # Schritt 4: Nachricht an Slack senden
    send_slack_message(ai_message) 

if __name__ == "__main__":
    main(LAT,LON)