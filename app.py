import os
from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
key = os.getenv('OPENWEATHER_API_KEY')


def get_weather(city):
    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': city,
        'appid': key,
        'units': 'metric',
        'lang': 'ru'
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return {
            'city': data['name'],
            'temp': round(data['main']['temp']),
            'feels_like': round(data['main']['feels_like']),
            'description': data['weather'][0]['description'],
            'humidity': data['main']['humidity'],
            'wind': data['wind']['speed'],
            'icon': data['weather'][0]['icon']
        }
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather')
def weather():
    city = request.args.get('city', '')

    if not city:
        return render_template('index.html', error='Введите город')

    data = get_weather(city)

    if data is None:
        return render_template('index.html', error='Город не найден')

    return render_template('index.html', weather=data)

if __name__ == '__main__':
    app.run(debug=True)