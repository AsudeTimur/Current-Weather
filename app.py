from flask import Flask, render_template, request
import requests
import plotly.graph_objs as go

app = Flask(__name__)

def get_weather_by_coordinates(latitude, longitude):
    API_KEY = '3ea9ff514429a6caa63af98b9e11c9ea'
    url = f'http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        weather_description = data['weather'][0]['description']
        return temperature, weather_description
    else:
        return None, None

def get_all_cities():
    # Burada tüm dünya şehirlerinin koordinatlarını alacak bir yöntem olmalıdır.
    # Bu örnek için sabit koordinatlar kullanalım.
    # Dünya genelinde rastgele birkaç şehir için örnek koordinatlar:
    cities = [
        {'name': 'New York', 'latitude': 40.7128, 'longitude': -74.0060},
        {'name': 'London', 'latitude': 51.5074, 'longitude': -0.1278},
        {'name': 'Tokyo', 'latitude': 35.6895, 'longitude': 139.6917}
    ]
    return cities

@app.route('/')
def index():
    cities = get_all_cities()
    
    # Hava durumu verilerini göstermek için bir Scattermapbox grafiği oluşturma
    figure = go.Figure()
    
    for city in cities:
        city_name = city['name']
        latitude = city['latitude']
        longitude = city['longitude']
        temperature, weather_description = get_weather_by_coordinates(latitude, longitude)
        
        figure.add_trace(go.Scattermapbox(
            lat=[latitude],
            lon=[longitude],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=14
            ),
            text=[f'{city_name}: {temperature}°C, {weather_description}'],
            name=city_name
        ))

    figure.update_layout(
        title='Hava Durumu Haritası',
        mapbox=dict(
            accesstoken='pk.eyJ1IjoiemV5bmVwYWtzb3kiLCJhIjoiY2x2MnRxcWVtMG05NDJubzFkbzNzdmg5YyJ9.qZVpgdncIf3bgQRFn8AOCg',  # Plotly'de bir hesap oluşturarak elde edebilirsiniz
            zoom=2
        ),
        width=1400,  # Genişlik ayarı
        height=900  # Yükseklik ayarı
    )

    return render_template('index.html', plot=figure.to_html(full_html=False))

if __name__ == '__main__':
    app.run(debug=True)
