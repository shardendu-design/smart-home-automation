import sys
import io
sys.path.insert(0, 'src')
from train import temp_pred_model,humid_pred_model,co2_pred_model,voc_pred_model,pm25_pred_model
import datetime
import pandas as pd
import time
import requests
import csv
import numpy as np
from sklearn.impute import SimpleImputer
import os

url = os.environ.get('API_LINK')

predicted_data = []

def live_sensor_data():

    sensor_data = []
    Url = url # api url path
    request = requests.request("GET", Url)
    data = request.json()
    add_new_col = {'location':'Janonhanta1,Vantaa,Finland'}

    add_bew_col_serial = {}
    data.update(add_bew_col_serial)
    data.update(add_new_col)
    sensor_data.append(data)
    
    return sensor_data



def temp_test_prediction():
    # Predict temperature for new data

    # Retrieve live sensor data
    live_data = live_sensor_data()

    # Create DataFrame
    df = pd.DataFrame(live_data)
    
    # Select relevant columns
    selected_real_time_data = df[['humid', 'co2', 'voc', 'pm25']]

    # Drop NaN values and duplicates
    selected_real_time_data = selected_real_time_data.dropna().drop_duplicates()

    # Set column names
    selected_real_time_data.columns = ['humid', 'co2', 'voc', 'pm25']  # Assign appropriate column names

    # Impute missing values if any
    imputer = SimpleImputer(strategy='mean')  # Use appropriate strategy
    selected_real_time_data_imputed = imputer.fit_transform(selected_real_time_data)

    # Retrieve current time
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    predicted_data.append({"DateTime": current_time})

    # Load temperature prediction model
    model_temp, score = temp_pred_model()
    predicted_data.append({"Tempe_Test_S": score})

    # Make predictions
    prediction_temperature = model_temp.predict(selected_real_time_data_imputed)
    extracted_value = prediction_temperature[0]
    predicted_data.append({"Temp_Pred": extracted_value})

    return extracted_value

def humid_test_prediction():
    # Predict humidity for new data

    # Retrieve live sensor data
    live_data = live_sensor_data()

    # Create DataFrame
    df1 = pd.DataFrame(live_data)
    
    # Select relevant columns
    selected_real_time_data_humid = df1[['temp', 'co2', 'voc', 'pm25']]

    # Drop NaN values and duplicates
    selected_real_time_data_humid = selected_real_time_data_humid.dropna().drop_duplicates()

    # Set column names
    selected_real_time_data_humid.columns = ['temp', 'co2', 'voc', 'pm25']  # Assign appropriate column names

    # Impute missing values if any
    imputer = SimpleImputer(strategy='mean')  # Use appropriate strategy
    selected_real_time_data_humid_imputed = imputer.fit_transform(selected_real_time_data_humid)

    # Retrieve current time
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    predicted_data.append({"DateTime": current_time})

    # Load humidity prediction model
    model_humid, score = humid_pred_model()
    predicted_data.append({"Humid_Test_S": score})

    # Make predictions
    prediction_humid = model_humid.predict(selected_real_time_data_humid_imputed)
    extracted_value = prediction_humid[0]
    predicted_data.append({"Humid_Pred": extracted_value})

    return extracted_value

def co2_test_prediction():
    # Predict CO2 for new data

    # Retrieve live sensor data
    live_data = live_sensor_data()
    
    # Create DataFrame
    df2 = pd.DataFrame(live_data)
    
    # Select relevant columns
    selected_real_time_data_co2 = df2[['temp', 'humid', 'voc', 'pm25']]

    # Drop NaN values and duplicates
    selected_real_time_data_co2 = selected_real_time_data_co2.dropna().drop_duplicates()

    # Set column names
    selected_real_time_data_co2.columns = ['temp', 'humid', 'voc', 'pm25']  # Assign appropriate column names

    # Impute missing values if any
    imputer = SimpleImputer(strategy='mean')  # Use appropriate strategy
    selected_real_time_data_co2_imputed = imputer.fit_transform(selected_real_time_data_co2)

    # Retrieve current time
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    predicted_data.append({"DateTime": current_time})

    # Load CO2 prediction model
    model_co2, mse = co2_pred_model()
    predicted_data.append({"Co2_Test_S": mse})

    # Make predictions
    prediction_co2 = model_co2.predict(selected_real_time_data_co2_imputed)
    extracted_value = prediction_co2[0]
    predicted_data.append({"Co2_Pred": extracted_value})

    return extracted_value

def voc_test_prediction():
    # Predict VOC for new data

    # Retrieve live sensor data
    live_data = live_sensor_data()

    # Create DataFrame
    df3 = pd.DataFrame(live_data)
    
    # Select relevant columns
    selected_real_time_data_voc = df3[['temp', 'humid', 'co2', 'pm25']]

    # Drop NaN values and duplicates
    selected_real_time_data_voc = selected_real_time_data_voc.dropna().drop_duplicates()

    # Set column names
    selected_real_time_data_voc.columns = ['temp', 'humid', 'co2', 'pm25']  # Assign appropriate column names

    # Retrieve current time
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    predicted_data.append({"DateTime": current_time})

    # Load VOC prediction model
    model_voc, mse = voc_pred_model()
    predicted_data.append({"VOC_Test_S": mse})

    # Convert DataFrame to NumPy array after setting column names
    selected_real_time_data_voc_array = selected_real_time_data_voc.to_numpy()

    # Make predictions using array without feature names
    prediction_voc = model_voc.predict(selected_real_time_data_voc_array)
    extracted_value = prediction_voc[0]
    predicted_data.append({"VOC_Pred": extracted_value})

    return extracted_value

def pm25_test_prediction():
    # Predict PM2.5 for new data

    # Retrieve live sensor data
    live_data = live_sensor_data()

    # Create DataFrame
    df4 = pd.DataFrame(live_data)
    
    # Select relevant columns
    selected_real_time_data_pm25 = df4[['temp', 'humid', 'co2', 'voc']]

    # Drop NaN values and duplicates
    selected_real_time_data_pm25 = selected_real_time_data_pm25.dropna().drop_duplicates()

    # Set column names
    selected_real_time_data_pm25.columns = ['temp', 'humid', 'co2', 'voc']  # Assign appropriate column names

    # Impute missing values if any
    imputer = SimpleImputer(strategy='mean')  # Use appropriate strategy
    selected_real_time_data_pm25_imputed = imputer.fit_transform(selected_real_time_data_pm25)

    # Retrieve current time
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    predicted_data.append({"DateTime": current_time})

    # Load PM2.5 prediction model
    model_pm25, mse = pm25_pred_model()
    predicted_data.append({"Pm25_Test_S": mse})

    # Make predictions
    prediction_pm25 = model_pm25.predict(selected_real_time_data_pm25_imputed)
    extracted_value = prediction_pm25[0]
    predicted_data.append({"Pm25_Pred": extracted_value})

    return extracted_value

