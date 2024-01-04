import time
from flask import render_template,request
from app.Indoor_air_quality import main  # Adjust the import based on your package structure
from src.current_weather_outdoor import current_weather_outside
from src.sensor_api import sensor_api_connection
from main import model_execution_with_live_data
from flask_login import login_required
import warnings
import csv 
import os

predicted_csv = os.environ.get('predicted_data')

def suppress_warnings(): 
    warnings.filterwarnings(action='ignore', category=UserWarning, module='sklearn')


    
@main.route('/dashboard')
@login_required
def display_dashboard():
    weather_data = current_weather_outside.outdoor_weather()
    sensor_data = sensor_api_connection.awair_api_call()
    
    filename = predicted_csv
    headers = []  # Initialize headers variable
    recent_row = []  # Initialize recent_row variable

    try:
        with open(filename, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            csv_data = list(csv_reader)  # Read all rows into csv_data

        if csv_data:
            headers = csv_data[0]  # Assuming the first row is headers
            recent_row = csv_data[-1]  # Getting the most recent row
    except FileNotFoundError:
        pass  # Handle the file not found error here if needed

    return render_template('home.html', weather_data=weather_data, sensor_data=sensor_data, headers=headers, recent_row=recent_row)


@main.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

