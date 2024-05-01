import time
from flask import render_template,request,redirect
from app.Indoor_air_quality import main  # Adjust the import based on your package structure
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
from src.WiFi_Socket import tapo_socket
from src.models.evaluate_models import perform_linear_regression, perform_random_forest, perform_support_vector_machine, perform_k_nearest_neighbors, perform_decision_trees
from notebook.exploratory_data_analysis import generate_base64_plot,generate_correlation_heatmap
import numpy as np
import pytz





predicted_csv = os.environ.get('predicted_data')
weather_csv_data = os.environ.get('weather_csv_data')
CSV_FILE = os.environ.get('CSV_FILE')
energy_cal_start_time = os.environ.get('energy_cal_start_time')
electricity_cost = os.environ.get('electricity_cost')
processed_data = os.environ.get('load_processed_data')

def suppress_warnings(): 
    warnings.filterwarnings(action='ignore', category=UserWarning, module='sklearn')
    
@main.route('/dashboard')
@login_required
def display_dashboard():
    

    device_id = os.environ.get('device_id')
    access_token = os.environ.get('access_token_smartthings')
    is_on = tapo_socket.device_status(access_token, device_id)
    

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

        csv_file_path = os.environ.get('CSV_FILE')  # Get file path from environment variable
        if not csv_file_path:
            return "CSV file path not found in environment variables", 404

        last_row_dict = {}
        with open(csv_file_path, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                if row:
                    last_row_dict = row  # Store the current row in the dictionary

        # Convert last_row_dict to a list of a single dictionary
        sensor_data = [last_row_dict] if last_row_dict else []

        weather_csv_data_path = os.environ.get('weather_csv_data')
        if not weather_csv_data_path:
            return "CSV file path not found in environment variables", 404
        last_row_dict_weather = {}
        with open(weather_csv_data_path, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                if row:
                    last_row_dict_weather = row
        weather_data = [last_row_dict_weather] if last_row_dict_weather else []
        
    except FileNotFoundError:
        pass  # Handle the file not found error here if needed


    return render_template('home.html', weather_data=weather_data, sensor_data=sensor_data, headers=headers, recent_row=recent_row, csv_data=csv_data,air_cooler_status=is_on)

@main.route('/dashboard/status')
@login_required
def display_device_info():
    
    
    device_id = os.environ.get('device_id')
    access_token = os.environ.get('access_token_smartthings')
    is_on = tapo_socket.device_status(access_token, device_id)

    device_info, switch_status, switch_timestamp = process_device_info()
    return render_template('device_info.html', device_info=device_info, switch_status=switch_status, switch_timestamp=switch_timestamp,air_cooler_status=is_on,)

@main.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@main.route('/latest-data')
@login_required
def latest_data():
    try:
        # Replace with the actual path to your CSV file
        df = pd.read_csv(predicted_csv)  # Read entire CSV file
        df = df.tail(100)  # Get the last 100 rows
        return jsonify(df.to_dict(orient='records'))
    except FileNotFoundError:
        return jsonify([])  # Return empty list if file not found


  
@main.route('/weather-data')
@login_required
def weather_data():
    try:
        # Replace with the actual path to your CSV file
        df = pd.read_csv(weather_csv_data)  # Read entire CSV file
        df = df.tail(100)  # Get the last 100 rows
        return jsonify(df.to_dict(orient='records'))
    except FileNotFoundError:
        return jsonify([])  # Return empty list if file not found


@main.route('/energy-data')
@login_required
def energy_data():
    try:
        # Replace with the actual path to your CSV file
        df = pd.read_csv(electricity_cost) # Read entire CSV file
        df = df.tail(100)  # Get the last 100 rows
        return jsonify(df.to_dict(orient='records'))
    except FileNotFoundError:
        return jsonify([])  # Return empty list if file not found

@main.route('/sensor-data')
@login_required
def sensor_data():
    try:
        # Replace with the actual path to your CSV file
        df = pd.read_csv(CSV_FILE,low_memory=False)  # Read entire CSV file
        df = df.tail(100)  # Get the last 100 rows
        return jsonify(df.to_dict(orient='records'))
    except FileNotFoundError:
        return jsonify([])  # Return empty list if file not found


        
@main.route('/display-sensor-data')
@login_required
def display_sensor_data():

    device_id = os.environ.get('device_id')
    access_token = os.environ.get('access_token_smartthings')
    is_on = tapo_socket.device_status(access_token, device_id)
    
    search_query = request.args.get('search', '')  # Get the search query
    page = request.args.get('page', 1, type=int)
    per_page = 20

    data = pd.read_csv(CSV_FILE,low_memory=False)

    local_tz = pytz.timezone('Europe/Helsinki')

    # # Handling ISO 8601 format timestamps
    # iso_8601_mask = data['timestamp'].str.endswith('Z')
    # data.loc[iso_8601_mask, 'timestamp'] = pd.to_datetime(data.loc[iso_8601_mask, 'timestamp']).dt.tz_convert(local_tz).dt.strftime('%Y-%m-%d %H:%M:%S')

    # # Handling other formats (assuming they are already in local time)
    # other_timestamps_mask = ~iso_8601_mask
    # data.loc[other_timestamps_mask, 'timestamp'] = pd.to_datetime(data.loc[other_timestamps_mask, 'timestamp'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')

    if search_query:
        # Convert 'timestamp' to string for searching
        data['timestamp'] = data['timestamp'].astype(str)

        # Filter the data based on the search query
        data = data[data['timestamp'].str.contains(search_query, case=False, na=False)]

    total_rows = len(data)
    total_pages = (total_rows - 1) // per_page + 1

    data_subset = data.iloc[(page - 1) * per_page : page * per_page]
    data_dicts = data_subset.to_dict(orient='records')
    return render_template('awair_sensor.html', table=data_dicts, total_pages=total_pages, current_page=page, air_cooler_status=is_on)

@main.route('/display-predicted-data')
@login_required
def display_predicted_data():

    device_id = os.environ.get('device_id')
    access_token = os.environ.get('access_token_smartthings')
    is_on = tapo_socket.device_status(access_token, device_id)
    
    search_query = request.args.get('search', '')  # Get the search query
    page = request.args.get('page', 1, type=int)
    per_page = 20

    data = pd.read_csv(predicted_csv)

   # Assuming your 'DateTime' column is in UTC
    local_tz = pytz.timezone('Europe/Helsinki')  # Adjust timezone as needed
    # data['DateTime'] = pd.to_datetime(data['DateTime']).dt.tz_localize('utc').dt.tz_convert(local_tz).dt.strftime('%Y-%m-%d %H:%M:%S')

    
    
    # Round 'Temp_Pred' and 'Humid_Pred' columns to two decimal places
    if 'Temp_Pred' in data.columns:
        data['Temp_Pred'] = data['Temp_Pred'].round(2)
    if 'Humid_Pred' in data.columns:
        data['Humid_Pred'] = data['Humid_Pred'].round(2)
    if 'Tempe_Test_S' in data.columns:
        data['Tempe_Test_S'] = data['Tempe_Test_S'].round(2)
    if 'Humid_Test_S' in data.columns:
        data['Humid_Test_S'] = data['Humid_Test_S'].round(2)
    if 'Co2_Test_S' in data.columns:
        data['Co2_Test_S'] = data['Co2_Test_S'].round(2)
    if 'VOC_Test_S' in data.columns:
        data['VOC_Test_S'] = data['VOC_Test_S'].round(2)
    if 'Pm25_Test_S' in data.columns:
        data['Pm25_Test_S'] = data['Pm25_Test_S'].round(2)

    if search_query:
        # Filter the data based on the search query
        # Adjust the filtering logic based on your data structure and needs
        data = data[data['DateTime'].str.contains(search_query, case=False)]

    total_rows = len(data)
    total_pages = (total_rows - 1) // per_page + 1

    data_subset = data.iloc[(page - 1) * per_page : page * per_page]
    data_dicts = data_subset.to_dict(orient='records')
    return render_template('ml_prediction.html', table=data_dicts, total_pages=total_pages, current_page=page, air_cooler_status=is_on)

@main.route('/display-energy-data')
@login_required
def display_energy_data():

    device_id = os.environ.get('device_id')
    access_token = os.environ.get('access_token_smartthings')
    is_on = tapo_socket.device_status(access_token, device_id)
    
    search_query = request.args.get('search', '')  # Get the search query
    page = request.args.get('page', 1, type=int)
    per_page = 5

    data = pd.read_csv(electricity_cost)

    # utc = pytz.utc
    local_tz = pytz.timezone('Europe/Helsinki')  # replace with your local timezone

    # Convert and format the Start_time and End_time columns
    data['Start_time'] = pd.to_datetime(data['Start_time']).dt.tz_convert(local_tz).dt.strftime('%Y-%m-%d %H:%M:%S')
    data['End_time'] = pd.to_datetime(data['End_time']).dt.tz_convert(local_tz).dt.strftime('%Y-%m-%d %H:%M:%S')

    # Create a concatenated column for searching
    data['combined_time'] = data['Start_time'].astype(str) + '-' + data['End_time'].astype(str)

    

    if search_query:
        # Filter the data based on the search query
        # Adjust the filtering logic based on your data structure and needs
        # Filter the data based on the search query in the concatenated column
        data = data[data['combined_time'].str.contains(search_query, case=False, na=False)]

    total_rows = len(data)
    total_pages = (total_rows - 1) // per_page + 1

    data_subset = data.iloc[(page - 1) * per_page : page * per_page]
    data_dicts = data_subset.to_dict(orient='records')
    return render_template('energy_cost.html', table=data_dicts, total_pages=total_pages, current_page=page, air_cooler_status=is_on)

@main.route('/display-weather-data')
@login_required
def display_weather_data():

    device_id = os.environ.get('device_id')
    access_token = os.environ.get('access_token_smartthings')
    is_on = tapo_socket.device_status(access_token, device_id)
    
    search_query = request.args.get('search', '')  # Get the search query
    page = request.args.get('page', 1, type=int)
    per_page = 20

    data = pd.read_csv(weather_csv_data)

    # Assuming your timestamps are in a column named 'Timestamp' and are in UTC
    utc = pytz.utc
    local_tz = pytz.timezone('Europe/Helsinki')  # replace with your local timezone

    # Convert timestamps to local timezone
    # data['Timestamp'] = pd.to_datetime(data['Timestamp']).dt.tz_localize(utc).dt.tz_convert(local_tz).dt.strftime('%Y-%m-%d %H:%M:%S')

    if search_query:
        # Filter the data based on the search query
        # Adjust the filtering logic based on your data structure and needs
        data = data[data['Timestamp'].str.contains(search_query, case=False)]

    total_rows = len(data)
    total_pages = (total_rows - 1) // per_page + 1

    data_subset = data.iloc[(page - 1) * per_page : page * per_page]
    data_dicts = data_subset.to_dict(orient='records')
    return render_template('weather.html', table=data_dicts, total_pages=total_pages, current_page=page, air_cooler_status=is_on)


@main.route('/display-about-project')
@login_required
def display_about_project():
    device_id = os.environ.get('device_id')
    access_token = os.environ.get('access_token_smartthings')
    is_on = tapo_socket.device_status(access_token, device_id)

    return render_template('about-project.html', air_cooler_status=is_on)


@main.route('/pick-model', methods=['GET', 'POST'])
@login_required
def pick_model():
    device_id = os.environ.get('device_id')
    access_token = os.environ.get('access_token_smartthings')
    is_on = tapo_socket.device_status(access_token, device_id)

    evaluation_result = None  # Initialize evaluation result
    
    if request.method == 'POST':
        selected_model = request.form.get('model')  # Get the selected model
        # Perform evaluation based on the selected model
        if selected_model == 'linear-regression':
            # Perform linear regression evaluation
            evaluation_result = perform_linear_regression()
        # Add other model evaluations here...
        elif selected_model == 'random-forest':
            evaluation_result = perform_random_forest()

        elif selected_model == 'support-vector-machine':
            # Perform support vector machine evaluation
            evaluation_result = perform_support_vector_machine()
        elif selected_model == 'k-nearest-neighbors':
            # Perform k-nearest neighbors evaluation
            evaluation_result = perform_k_nearest_neighbors()
        elif selected_model == 'decision-trees':
            evaluation_result = perform_decision_trees()
        else:
            # Handle invalid model selection
            return render_template('error.html', message='Invalid model selection')

    return render_template('pick-model.html', air_cooler_status=is_on, evaluation_result=evaluation_result)

@main.route('/data-analysis')
@login_required
def data_analysis():
    device_id = os.environ.get('device_id')
    access_token = os.environ.get('access_token_smartthings')
    is_on = tapo_socket.device_status(access_token, device_id)

    awair_csv_file = os.environ.get('CSV_FILE')
    awair_csv_data = pd.read_csv(awair_csv_file)
    
    # Create a copy of the slice for safe modification
    selected_required_columns = awair_csv_data[['temp', 'humid', 'co2', 'voc', 'pm25']].copy()
    selected_required_columns.drop_duplicates(inplace=True)
    selected_required_columns.dropna(inplace=True)
    # Calculate correlation matrix
    correlation_matrix = selected_required_columns.corr()

    # Generate heatmap
    correlation_heatmap = generate_correlation_heatmap(correlation_matrix)

    # Generate plots
    # Generate plots
    plots = {
    'temp': generate_base64_plot(selected_required_columns, 'temp', 'blue', 'Temperature Distribution', 'Temperature (°C)'),
    'humid': generate_base64_plot(selected_required_columns, 'humid', 'green', 'Humidity Distribution', 'Humidity'),
    'co2': generate_base64_plot(selected_required_columns, 'co2', 'pink', 'Co2 Distribution', 'Co2'),
    'voc': generate_base64_plot(selected_required_columns, 'voc', 'red', 'VOC Distribution', 'VOC'),
    'pm25': generate_base64_plot(selected_required_columns, 'pm25', 'yellow', 'Pm2.5 Distribution', 'Pm2.5'),

    # Add other variables here...
    }
    
    return render_template('exploratory_analysis.html', plots=plots, correlation_heatmap=correlation_heatmap, air_cooler_status=is_on)

@main.route('/system-design-tech')
@login_required
def system_design_tech():
    device_id = os.environ.get('device_id')
    access_token = os.environ.get('access_token_smartthings')
    is_on = tapo_socket.device_status(access_token, device_id)

    return render_template('system-design-tech.html', air_cooler_status=is_on)

@main.route('/contact')
@login_required
def contact():
    device_id = os.environ.get('device_id')
    access_token = os.environ.get('access_token_smartthings')
    is_on = tapo_socket.device_status(access_token, device_id)

    return render_template('contact.html', air_cooler_status=is_on)

# device turn off through dashboard button
@main.route('/stop-device', methods=['POST'])
@login_required
def stop_device():
    # Add logic here to trigger the air_cooler_power_off function
    turn_off_device = tapo_socket.air_cooler_power_turn_off()
    
    return jsonify({'message': 'Device stopped successfully'})

@main.route('/add-new-device')
@login_required
def add_new_device():
    device_id = os.environ.get('device_id')
    access_token = os.environ.get('access_token_smartthings')
    is_on = tapo_socket.device_status(access_token, device_id)
    return render_template('add_new_device.html',air_cooler_status=is_on)