import pyowm
owm = pyowm.OWM('29139e44afaa3ce82a43eb2e2b06d033')
weather_mgr = owm.weather_manager()
place = 'Vantaa, FI'
observation = weather_mgr.weather_at_place(place)
temperature = observation.weather.temperature("celsius")["temp"]
humidity = observation.weather.humidity
wind = observation.weather.wind()
print(f'Temperature: {temperature}°C')
print(f'Humidity: {humidity}%')
print(f'Wind Speed: {wind["speed"]} m/s')


import requests

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

    # Print the full current weather data
    print(data)

else:
    print(f"Error fetching weather data. Status code: {response.status_code}")