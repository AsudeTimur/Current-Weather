from flask import Flask, render_template
import requests

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
        'clear sky': 'Açık Hava',
        'few clouds': 'Az Bulutlu',
        'scattered clouds': 'Parçalı Bulutlu',
        'broken clouds': 'Kırık Bulutlu',
        'overcast clouds': 'Kapalı Bulutlu',
        'light rain': 'Hafif Yağmur',
        'moderate rain': 'Orta Şiddetli Yağmur',
        'heavy intensity rain': 'Yoğun Yağış',
        'shower rain': 'Sağanak Yağış',
        'thunderstorm': 'Gök Gürültülü Fırtına',
        'snow': 'Kar',
        'mist': 'Sis',
        'smoke': 'Duman',
        'haze': 'Puslu',
        'sand/ dust whirls': 'Kum/ Toz Hortumu',
        'fog': 'Sisli',
        'sand': 'Kumlu',
        'dust': 'Tozlu',
        'volcanic ash': 'Volkanik Kül',
        'squalls': 'Şiddetli Fırtına',
    }
    return translations.get(description, description)

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
        temperature, description, lon, lat = get_weather(city)
        if temperature is not None:
            weather_data.append({
                'city': city,
                'temperature': temperature,
                'description': description,
                'lon': lon,
                'lat': lat
            })

    return render_template('index.html', weather_data=weather_data)

if __name__ == '__main__':
    app.run(debug=True)
