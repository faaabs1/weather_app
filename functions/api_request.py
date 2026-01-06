import requests
from datetime import datetime,timedelta



BASE_URL = "https://dataset.api.hub.geosphere.at/v1/timeseries/forecast/nowcast-v1-15min-1km"



def get_available_parameters():
    """Helper to find out what data is available (Temp, Rain, Wind...)"""
    url = f"{BASE_URL}/metadata"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print("Available Parameters:")
        for param in data.get('parameters', []):
            print(f"- {param['name']}: {param.get('long_name', 'No description')} ({param.get('unit', '')})")
        return [p['name'] for p in data.get('parameters', [])]
    else:
        print(f"Error fetching metadata: {response.status_code}")
        return []
    

def get_forecast(lat, lon):
    """Fetches the actual weather data"""
    
    # Define the time range (e.g., next 2 hours)
    start_time = datetime.now().strftime("%Y-%m-%dT%H:%M")
    end_time = (datetime.now() + timedelta(hours=12)).strftime("%Y-%m-%dT%H:%M")

    params_to_fetch = "t2m,ff,rr" 
    
    query_params = {
        "lat_lon": f"{lat},{lon}",
        "parameters": params_to_fetch,
        "start": start_time,
        "end": end_time,
        "output_format": "geojson"
    }

    response = requests.get(BASE_URL, params=query_params)

    if response.status_code == 200:
        data = response.json()
        
        # Parsing the GeoJSON response
        features = data.get('features', [])
        if not features:
            print("No data found for this location.")
            return None
            
        timestamps = data['timestamps']
        properties = features[0]['properties']['parameters']
        
        print(f"\nForecast for Lat: {lat}, Lon: {lon}")
        
        # Simple print loop
        for i, time in enumerate(timestamps):
            temp = properties['t2m']['data'][i]
            rain = properties['rr']['data'][i]
            wind = properties['ff']['data'][i]
            print(f"{time}: Temp: {temp}°C, Rain: {rain}mm, Wind: {wind}km/h")
            
        return data
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None
    
def parse_weather_data(forecast_data):
    try:
        props = forecast_data['features'][0]['properties']['parameters']
        temp_val = props['t2m']['data'][0]
        rain_val = props['rr']['data'][0]
        wind_ms = props['ff']['data'][0]
        wind_kmh = round(wind_ms * 3.6, 1)  # Convert m/s to km/h

        rain_txt = "Kein Regen"
        if rain_val > 0:
            rain_txt = f"{rain_val}mm Regen"
            if rain_val > 0.5: rain_txt += ('Nass!')
            if rain_val > 4.0: rain_txt += (' Starkregen!')

        wetter_bericht = (
            f"Temperatur: {temp_val}°C, "
            f"Regen: {rain_txt}, "
            f"Wind: {wind_kmh}km/h"
        )

        return wetter_bericht
    except KeyError as e:
        return f"Fehler beim Lesen der Daten: Schlüssel {e} fehlt."
    except IndexError:
        return "Fehler: Keine Datenpunkte in der Liste."