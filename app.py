from flask import Flask, render_template
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
        weather_description = translate_weather_description(data['weather'][0]['description'])
        longitude = data['coord']['lon']
        latitude = data['coord']['lat']
        return temperature, weather_description, longitude, latitude
    else:
        return None, None, None, None

def translate_weather_description(description):
    translations = {
        'clear sky': 'açık hava',
        'few clouds': 'az bulutlu',
        'scattered clouds': 'parçalı bulutlu',
        'broken clouds': 'kırık bulutlu',
        'overcast clouds': 'kapalı bulutlu',
        'light rain': 'hafif yağmur',
        'moderate rain': 'orta şiddetli yağmur',
        'heavy intensity rain': 'yoğun yağış',
        'shower rain': 'sağanak yağış',
        'thunderstorm': 'gök gürültülü fırtına',
        'snow': 'kar',
        'mist': 'sis',
        'smoke': 'duman',
        'haze': 'puslu',
        'sand/ dust whirls': 'kum/ toz hortumu',
        'fog': 'sisli',
        'sand': 'kumlu',
        'dust': 'tozlu',
        'volcanic ash': 'volkanik kül',
        'squalls': 'şiddetli fırtına',
        'tornado': 'tornado'
        # İhtiyacınıza göre diğer hava durumu terimlerini buraya ekleyebilirsiniz
    }
    return translations.get(description, description)

def generate_weather_map():
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

    figure = go.Figure()

    for city in turkish_cities:
        temperature, weather_description, longitude, latitude = get_weather(city)
        if temperature is not None and weather_description is not None:
            figure.add_trace(go.Scattermapbox(
                lat=[latitude],
                lon=[longitude],
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size=10,
                    color='blue',
                    opacity=0.7
                ),
                text=f'{city}<br>Sıcaklık: {temperature}°C<br>Açıklama: {weather_description}',
                name=city
            ))

    figure.update_layout(
        title='Türkiye\'deki Şehirlerin Hava Durumu Haritası',
        mapbox=dict(
            style='carto-positron',
            zoom=5,
            center=dict(lat=39.9255, lon=32.8667)
        ),
        width=1400,
        height=800
    )

    return figure

@app.route('/')
def index():
    weather_map = generate_weather_map()
    return render_template('index.html', plot=weather_map.to_html(full_html=False))

if __name__ == '__main__':
    app.run(debug=True)
