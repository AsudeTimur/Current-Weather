# app.py dosyası
from flask import Flask, render_template, request
import requests
import plotly.graph_objs as go

app = Flask(__name__)

def get_weather(city):
    API_KEY = '3ea9ff514429a6caa63af98b9e11c9ea'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        weather_description = data['weather'][0]['description']
        longitude = data['coord']['lon']
        latitude = data['coord']['lat']
        return temperature, weather_description, longitude, latitude
    else:
        return None, None, None, None

@app.route('/')
def index():
    city = 'Istanbul'
    temperature, weather_description, longitude, latitude = get_weather(city)
    
    # Hava durumu verilerini göstermek için bir Scattermapbox grafiği oluşturma
    figure = go.Figure(go.Scattermapbox(
        lat=[latitude],
        lon=[longitude],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=14
        ),
        text=[f'{temperature}°C, {weather_description}'],
    ))

    figure.update_layout(
        title='Hava Durumu Haritası',
        mapbox=dict(
            accesstoken='YOUR_MAPBOX_ACCESS_TOKEN_HERE',  # Plotly'de bir hesap oluşturarak elde edebilirsiniz
            center=dict(lat=latitude, lon=longitude),
            zoom=10
        )
    )

    return render_template('index.html', temperature=temperature, weather_description=weather_description, plot=figure.to_html(full_html=False))

if __name__ == '__main__':
    app.run(debug=True)
