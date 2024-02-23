import time
from flask import render_template,request
from app.Indoor_air_quality import main  # Adjust the import based on your package structure
from src.current_weather_outdoor import current_weather_outside
from src.sensor_api import sensor_api_connection
from main import model_execution_with_live_data
from seperate import process_device_info
from flask_login import login_required
import warnings
import csv 
import os
from flask import jsonify
import pandas as pd
import csv
import traceback

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
    csv_data = []  # Initialize csv_data

    try:
        with open(filename, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                # Convert each row to string to ensure JSON serialization
                csv_data.append([str(item) for item in row])

        if csv_data:
            headers = csv_data[0]  # Assuming the first row is headers
            recent_row = csv_data[-1]  # Getting the most recent row
    except FileNotFoundError:
        pass  # Handle the file not found error here if needed

    return render_template('home.html', weather_data=weather_data, sensor_data=sensor_data, headers=headers, recent_row=recent_row, csv_data=csv_data)

@main.route('/dashboard/status')
@login_required
def display_device_info():
    device_info, switch_status, switch_timestamp = process_device_info()
    return render_template('device_info.html', device_info=device_info, switch_status=switch_status, switch_timestamp=switch_timestamp)

@main.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@main.route('/latest-data')
@login_required
def latest_data():
    try:
        # Replace with the actual path to your CSV file
        df = pd.read_csv(predicted_csv, nrows=100)  # Reading last 100 rows
        return jsonify(df.to_dict(orient='records'))
    except FileNotFoundError:
        return jsonify([])  # Return empty list if file not found


  
@main.route('/weather-data')
@login_required
def weather_data():
    try:
        weather_data_list = current_weather_outside.outdoor_weather()  # This is a list of dictionaries
        return jsonify(weather_data_list)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify([])  # Return empty list if any error occurs
