from flask import Flask, render_template, request
import requests
import openai
import config

app = Flask(__name__)

# Obtenir les données météo via l'API OpenWeather
def get_weather_data(city_name):
    api_key = config.OPENWEATHER_API_KEY
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Générer un rapport météo avec GPT-4
def generate_weather_report(weather_data):
    openai.api_key = config.OPENAI_API_KEY

    description = weather_data['weather'][0]['description']
    temp = weather_data['main']['temp']
    humidity = weather_data['main']['humidity']
    wind_speed = weather_data['wind']['speed']

    prompt = f"Rédige un rapport météo pour une ville. Voici les données : Description : {description}, Température : {temp}°C, Humidité : {humidity}%, Vitesse du vent : {wind_speed} km/h. Le rapport doit être clair et utile pour un utilisateur non technique."

    response = openai.Completion.create(
        engine="gpt-4",
        prompt=prompt,
        max_tokens=150
    )

    return response.choices[0].text.strip()

# Route principale
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city_name = request.form['city']
        weather_data = get_weather_data(city_name)
        if weather_data:
            report = generate_weather_report(weather_data)
            return render_template('index.html', report=report, city=city_name)
        else:
            return render_template('index.html', error="Impossible de récupérer les données météo.")
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
