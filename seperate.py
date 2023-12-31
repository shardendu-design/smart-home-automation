import time
from src.current_weather_outdoor import current_weather_outside
# Your outdoor_weather function remains unchanged

# Function to fetch weather data and display it
def fetch_and_display_weather():
    weather_data =  current_weather_outside.outdoor_weather()
    print(weather_data)  # For debugging or verification purposes
    
    # Insert code here to display or use the weather_data fetched

# To test and display data, call the function in a loop
while True:
    fetch_and_display_weather()
    time.sleep(600)  # Wait for 10 minutes before fetching data again
