import time
from flask import render_template
from app.Indoor_air_quality import main  # Adjust the import based on your package structure
from src.current_weather_outdoor import current_weather_outside

from flask_login import login_required

@main.route('/dashboard')
@login_required
def display_dashboard():
    return render_template('home.html')

@main.route('/weather')
@login_required
def weather_display():
    weather_data = current_weather_outside.outdoor_weather()
    time.sleep(600)
    return render_template('weather.html', weather_data=weather_data)

     
@main.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

