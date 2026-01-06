from google import genai
import os
from dotenv import load_dotenv

def generate_ai_message(weather_data_string):
    """
    Nimmt den Wetter-String (z.B. "Temp: 12C, Rain: 0mm") 
    und macht daraus eine coole Nachricht.
    """
    
    load_dotenv()
    api_key = os.getenv('GEMINI_API_KEY')

    client = genai.Client(api_key=api_key)

    # Der Prompt ist das Wichtigste! Hier geben wir der KI ihre Persönlichkeit.
    prompt = f"""
    Du bist mein persönlicher Morgen-Assistent auf meinem Handy.
    
    Hier sind die harten Fakten für heute Morgen:
    {weather_data_string}
    
    Deine Aufgabe:
    Schreibe eine kurze Push-Benachrichtigung (maximal 250 Zeichen).
    1. Sei locker und motivierend (du darfst "Du" sagen).
    2. Erwähne das Wetter nur kurz und gib mir einen Ausblick auf den Tag.
    3. Gib mir eine klare Kleidungsempfehlung (z.B. "Zwiebellook", "Dicke Jacke", "Sonnenbrille").
    4. Nutze passende Emojis.
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )
        return response.text
    except Exception as e:
        # HIER: Den Fehler ausgeben!
        print(f"⚠️ FEHLER BEI GEMINI: {e}")  
        return f"KI konnte nicht antworten, aber hier das Wetter: {weather_data_string}"