import time
from flask import render_template
from app.Indoor_air_quality import main  # Adjust the import based on your package structure
from src.current_weather_outdoor import current_weather_outside
from src.sensor_api import sensor_api_connection

from flask_login import login_required


@main.route('/dashboard')
@login_required
def display_dashboard():
    return render_template('home.html')

@main.route('/dashboard/weather')
@login_required
def weather_display():
    weather_data = current_weather_outside.outdoor_weather()
    # time.sleep(600)
    return render_template('weather.html', weather_data=weather_data)

@main.route('/dashboard/sensor-data')
@login_required
def awair_sensor_data():
    sensor_data = sensor_api_connection.awair_api_call()
    return render_template('awair_sensor.html', sensor_data=sensor_data)

@main.route('/dashboard/pred-data')
@login_required
def display_prediction():
    predicted_value = future_model
    if predicted_value is not None:
        return render_template('ml_predicion.html', predicted_value=predicted_value)
    else:
        # Handle the case when predicted_value is None
        return "No prediction available."

@main.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

