from flask import Flask, render_template
import requests
from folium import plugins
import folium
import numpy as np

app = Flask(__name__)

def get_weather(city):
    API_KEY = '3ea9ff514429a6caa63af98b9e11c9ea'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        longitude = data['coord']['lon']
        latitude = data['coord']['lat']
        return temperature, longitude, latitude
    else:
        return None, None, None

@app.route('/')
def index():
    turkish_cities = [
        'Adana', 'Adıyaman', 'Afyonkarahisar', 'Ağrı', 'Amasya', 'Ankara', 'Antalya', 'Artvin', 'Aydın', 'Balıkesir',
        'Bilecik', 'Bingöl', 'Bitlis', 'Bolu', 'Burdur', 'Bursa', 'Çanakkale', 'Çankırı', 'Çorum', 'Denizli',
        'Diyarbakır', 'Edirne', 'Elazığ', 'Erzincan', 'Erzurum', 'Eskişehir', 'Gaziantep', 'Giresun', 'Gümüşhane',
        'Hakkari', 'Hatay', 'Isparta', 'Mersin', 'İstanbul', 'İzmir', 'Kars', 'Kastamonu', 'Kayseri', 'Kırklareli',
        'Kırşehir', 'Kocaeli', 'Konya', 'Kütahya', 'Malatya', 'Manisa', 'Kahramanmaraş', 'Mardin', 'Muğla', 'Muş',
        'Nevşehir', 'Niğde', 'Ordu', 'Rize', 'Sakarya', 'Samsun', 'Siirt', 'Sinop', 'Sivas', 'Tekirdağ', 'Tokat',
        'Trabzon', 'Tunceli', 'Şanlıurfa', 'Uşak', 'Van', 'Yozgat', 'Zonguldak', 'Aksaray', 'Bayburt', 'Karaman',
        'Kırıkkale', 'Batman', 'Şırnak', 'Bartın', 'Ardahan', 'Iğdır', 'Yalova', 'Karabük', 'Kilis', 'Osmaniye',
        'Düzce'
    ]

    weather_data = []
    for city in turkish_cities:
        temperature, lon, lat = get_weather(city)
        if temperature is not None:
            weather_data.append({
                'temperature': temperature,
                'lon': lon,
                'lat': lat
            })

    # Create a map centered at Turkey's coordinates
    map = folium.Map(location=[39.9334, 32.8597], zoom_start=6)

    # Create a HeatMap layer using temperature data
    heat_data = [[data['lat'], data['lon'], data['temperature']] for data in weather_data]

    # Normalize temperature data to range between 0 and 1
    temperatures = [data['temperature'] for data in weather_data]
    normalized_temperatures = np.interp(temperatures, (min(temperatures), max(temperatures)), (0, 1))

    # Combine latitudes, longitudes, and normalized temperatures
    heat_data_normalized = [[data[0], data[1], normalized_temperatures[i]] for i, data in enumerate(heat_data)]

    # Create HeatMap with gradient
    plugins.HeatMap(heat_data_normalized, gradient={0.2: 'blue', 0.4: 'cyan', 0.6: 'yellow', 1: 'red'}, radius=15).add_to(map)

    # Save the map as HTML file
    map.save('templates/heatmap.html')

    return render_template('heatmap.html')

if __name__ == '__main__':
    app.run(debug=True)
