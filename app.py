from flask import Flask, render_template
import requests
from pymongo import MongoClient
import threading
import time
from bson import json_util
import json

app = Flask(__name__)

client = MongoClient('mongodb+srv://zaksoy852:zeynep23@cluster0.h9amh6f.mongodb.net/')
db = client.hava_veri
collection = db.hava_durum

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
        
        weather_data = {
            'city': city,
            'temperature': temperature,
            'description': weather_description,
            'longitude': longitude,
            'latitude': latitude
        }
        collection.update_one({'city': city}, {'$set': weather_data}, upsert=True)
        
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
    }
    return translations.get(description, description)

def update_weather_data():
    while True:
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
        
        for city in turkish_cities:
            get_weather(city)
        
        time.sleep(300)  # 5 dakika bekle

@app.route('/')
def index():
    weather_data = list(collection.find())
    weather_data_json = json.loads(json_util.dumps(weather_data))
    return render_template('index.html', weather_data=weather_data_json)

if __name__ == '__main__':
    weather_update_thread = threading.Thread(target=update_weather_data)
    weather_update_thread.start()
    app.run(debug=True)