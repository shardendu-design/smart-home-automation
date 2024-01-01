import time
from src.current_weather_outdoor import current_weather_outside
from src.sensor_api import sensor_api_connection
from src.models import model_test_with_live_data
from shared_values import future_model

# Now you can use future_model as needed



def display_prediction():
      
      predicted_values = future_model
      print(predicted_values)  # For debugging or verification purposes
    

display_prediction()