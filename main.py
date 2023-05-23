import requests
import tkinter as tk
from configparser import ConfigParser


# Obtaining the API key
config = ConfigParser()
config.read('secrets.ini')
api_key = config.get('wgb', 'key')


def current_weather(city):
    """Fetching the current weather of the city"""

    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        desc = data['weather'][0]['description']

        forecast_result.config(text='')

        current_weather_result.config(
            text=f"Today's Weather in {city.upper()}:\n\nTemperature: {temp} °C\nHumidity: {humidity}%\nCondition: {desc}")
   
    else:
        current_weather_result.config(text='City not found.')


def get_forecast(city):
    """Fetching the 5-day weather forecast of the city"""

    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        forecasts = data['list']

        current_weather_result.config(text='')

        forecast_text = f'5-Days Weather Forecast in {city.upper()}:\n\n'

        for i in range(0, len(forecasts), 8):
            forecast = forecasts[i]
            date = forecast['dt_txt'].split()[0]
            temp = forecast['main']['temp']
            humidity = forecast['main']['humidity']
            desc = forecast['weather'][0]['description']

            forecast_text += f'Date: {date}\nTemperature: {temp} °C\nHumidity: {humidity}%\nWeather Description: {desc}\n{"-" * 30}\n'

        forecast_result.config(text=forecast_text)
   
    else:
        forecast_result.config(text='City not found.')


def handle_current_weather():
    """If input (city) is not provided"""
    city = city_entry.get().strip()
    if city:
        current_weather(city)
    else:
        current_weather_result.config(text='Please enter a city.')


def handle_forecast():
    """If input (city) is not provided"""
    city = city_entry.get().strip()
    if city:
        get_forecast(city)
    else:
        forecast_result.config(text='Please enter a city.')



# Tkinter
window = tk.Tk()
window.title("Weather App")

city_label = tk.Label(window, text="Enter the City: ", font=("Arial", 14))
city_label.pack(pady=10)

city_entry = tk.Entry(window, font=("Arial", 14))
city_entry.pack()

buttons_frame = tk.Frame(window)
buttons_frame.pack(pady=10)

current_weather_btn = tk.Button(buttons_frame, text="Current Weather", font=("Arial", 14),
                               command=handle_current_weather)
current_weather_btn.pack(side='left', padx=5)

forecast_btn = tk.Button(buttons_frame, text="5-day Forecast", font=("Arial", 14),
                         command=handle_forecast)
forecast_btn.pack(side='left', padx=5)

current_weather_label = tk.Label(window, font=("Arial", 14, "bold"))
current_weather_label.pack(pady=10)

current_weather_result = tk.Label(window, font=("Arial", 14), justify='left')
current_weather_result.pack()

forecast_label = tk.Label(window, font=("Arial", 14, "bold"))
forecast_label.pack(pady=10)

forecast_result = tk.Label(window, font=("Arial", 14), justify='left')
forecast_result.pack()

window.mainloop()
