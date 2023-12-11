import requests
from tabulate import tabulate

def outdoor_weather():

    # Replace 'YOUR_API_KEY' with your actual OpenWeatherMap API key
    api_key = '29139e44afaa3ce82a43eb2e2b06d033'

    # Replace 'New York' with the desired location for weather data
    location = 'Vantaa'

    # Define the API endpoint to get current weather data
    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"

    # Make the API request to get the weather data
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Check if the required fields exist before accessing them
        weather_main = data['weather'][0].get('main', '-')
        main_temp = data['main'].get('temp', '-')
        main_feels_like = data['main'].get('feels_like', '-')
        main_pressure = data['main'].get('pressure', '-')
        main_humidity = data['main'].get('humidity', '-')
        visibility = data.get('visibility', '-')
        wind_speed = data['wind'].get('speed', '-')
        snowfall = data.get('snow', {}).get('1h', '-')
        city_name = data.get('name', '-')
        country_code = data['sys'].get('country', '-')

        headers = ['Temperature', 'Feels like', 'Pressure', 'Humidity',
                'Visibility', 'Wind Speed', 'Snowfall', 'City Name', 'Country Code']

        zip_data = [
            (
                main_temp, main_feels_like, main_pressure, main_humidity,
                visibility, wind_speed, snowfall, city_name, country_code
            )
        ]

        print(tabulate(zip_data, headers, tablefmt='pretty'))
