import sys
import os

# Get the directory of the current file
current_dir = os.path.dirname(os.path.realpath(__file__))

# Get the parent directory (backend/src)
parent_dir = os.path.dirname(current_dir)

# Add the parent directory to sys.path
sys.path.append(parent_dir)
from train import temp_pred_model,humid_pred_model,co2_pred_model,voc_pred_model,pm25_pred_model
import datetime
import pandas as pd
import time
import requests
import csv
import numpy as np
from sklearn.impute import SimpleImputer
import os
import pytz
from datetime import datetime as dt

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
    df = pd.DataFrame(live_sensor_data())
    selected_real_time_data = df[['humid','co2','voc','pm25']]

    selected_real_time_data = selected_real_time_data.dropna()
    selected_real_time_data = selected_real_time_data.drop_duplicates()
    # predicted_data.append(selected_real_time_data)

    # Convert current time to Helsinki timezone
    helsinki_timezone = pytz.timezone('Europe/Helsinki')
    current_time_local = dt.now(helsinki_timezone).strftime('%Y-%m-%d %H:%M:%S')


    # print("===========================================================")
    # current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    predicted_data.append({"DateTime": current_time_local})
    # print(f"Current_time: {current_time}")
    # print('sensor_data')

    # print(selected_real_time_data)

    # print("===========================================================")

    # Predict temperature for new data
    model_temp, rmse, mae, r2 = temp_pred_model()
    predicted_data.append({"Temp_RMSE": "{:.2f}".format(rmse)})
    predicted_data.append({"Temp_MAE": "{:.2f}".format(mae)})
    predicted_data.append({"Temp_R2": "{:.2f}".format(r2)})
    temp_prediction = model_temp
    

    prediction_temperature = temp_prediction.predict(selected_real_time_data)
    extracted_value = round(prediction_temperature[0],2)
    # Format the extracted value to 2 decimal places
    # formatted_extracted_value = "{:.2f}".format(extracted_value)
    predicted_data.append({"Temp_Pred": extracted_value})
    # print(f"predicted_temperature: {extracted_value}")

    # print("===========================================================")
    return extracted_value


def humid_test_prediction():
    # Predict humidity for new data
    df1 = pd.DataFrame(live_sensor_data())
    selected_real_time_data_humid = df1[['temp','co2','voc','pm25']]

    selected_real_time_data_humid = selected_real_time_data_humid.dropna()
    selected_real_time_data_humid = selected_real_time_data_humid.drop_duplicates()

    # Convert current time to Helsinki timezone
    helsinki_timezone = pytz.timezone('Europe/Helsinki')
    current_time_local = dt.now(helsinki_timezone).strftime('%Y-%m-%d %H:%M:%S')


    # print("===========================================================")
    # current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    predicted_data.append({"DateTime": current_time_local})
    # print(f"Current_time: {current_time}")
    # print('Real time data from sensor for humidity prediction')

    # print(selected_real_time_data_humid)

    # print("===========================================================")
    model_humid, rmse, mae, r2 = humid_pred_model()
    predicted_data.append({"Humid_RMSE": "{:.2f}".format(rmse)})
    predicted_data.append({"Humid_MAE": "{:.2f}".format(mae)})
    predicted_data.append({"Humid_R2": "{:.2f}".format(r2)})
    humid_prediction = model_humid
    prediction_humid = humid_prediction.predict(selected_real_time_data_humid)
    extracted_value = round(prediction_humid[0],2)

    # Format the extracted value to 2 decimal places
    # formatted_extracted_value = "{:.2f}".format(extracted_value)
    predicted_data.append({"Humid_Pred": extracted_value})

    # print(f"Predicted humidity: {prediction_humid}")

    # print("===========================================================")
    return extracted_value

def co2_test_prediction():
    # Predict CO2 for new data

    df2 = pd.DataFrame(live_sensor_data())
    selected_real_time_data_co2 = df2[['temp','humid','voc','pm25']]

    selected_real_time_data_co2 = selected_real_time_data_co2.dropna()
    selected_real_time_data_co2 = selected_real_time_data_co2.drop_duplicates()
    # print("===========================================================")

    # Convert current time to Helsinki timezone
    helsinki_timezone = pytz.timezone('Europe/Helsinki')
    current_time_local = dt.now(helsinki_timezone).strftime('%Y-%m-%d %H:%M:%S')

    # current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    predicted_data.append({"DateTime": current_time_local})
    # print(f"Current_time: {current_time}")
    # print('Real time data from sensor for co2 prediction')

    # print(selected_real_time_data_co2)

    # print("===========================================================")
    model_co2, rmse, mae, r2 = co2_pred_model()
    predicted_data.append({"Co2_RMSE": "{:.2f}".format(rmse)})
    predicted_data.append({"Co2_MAE": "{:.2f}".format(mae)})
    predicted_data.append({"Co2_R2": "{:.2f}".format(r2)})
    co2_prediction = model_co2

    prediction_co2 = co2_prediction.predict(selected_real_time_data_co2)
    extracted_value = prediction_co2[0]
    predicted_data.append({"Co2_Pred": extracted_value})

    # print(f"Predicted co2: {prediction_co2}")

    # print("===========================================================")
    return extracted_value

def voc_test_prediction():
    # Predict VOC for new data

    df3 = pd.DataFrame(live_sensor_data())
    selected_real_time_data_voc = df3[['temp','humid','co2','pm25']]

    selected_real_time_data_voc = selected_real_time_data_voc.dropna()
    selected_real_time_data_voc = selected_real_time_data_voc.drop_duplicates()
    # print("===========================================================")

    # Convert current time to Helsinki timezone
    helsinki_timezone = pytz.timezone('Europe/Helsinki')
    current_time_local = dt.now(helsinki_timezone).strftime('%Y-%m-%d %H:%M:%S')

    # current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    predicted_data.append({"DateTime": current_time_local})
    # print(f"Current_time: {current_time}")
    # print('Real time data from sensor for voc prediction')

    # print(selected_real_time_data_voc)

    # print("===========================================================")
    model_voc, rmse, mae, r2 = voc_pred_model()
    predicted_data.append({"Voc_RMSE": "{:.2f}".format(rmse)})
    predicted_data.append({"Voc_MAE": "{:.2f}".format(mae)})
    predicted_data.append({"Voc_R2": "{:.2f}".format(r2)})
    voc_prediction = model_voc
    prediction_voc = voc_prediction.predict(selected_real_time_data_voc)
    extracted_value = prediction_voc[0]
    predicted_data.append({"VOC_Pred": extracted_value})

    # print(f"Predicted voc: {prediction_voc}")

    # print("===========================================================")
    return extracted_value 

def pm25_test_prediction():
    # Predict PM2.5 for new data

    df4 = pd.DataFrame(live_sensor_data())
    selected_real_time_data_pm25 = df4[['temp','humid','co2','voc']]

    selected_real_time_data_pm25 = selected_real_time_data_pm25.dropna()
    selected_real_time_data_pm25 = selected_real_time_data_pm25.drop_duplicates()
    # print("===========================================================")

    # Convert current time to Helsinki timezone
    helsinki_timezone = pytz.timezone('Europe/Helsinki')
    current_time_local = dt.now(helsinki_timezone).strftime('%Y-%m-%d %H:%M:%S')

    # current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    predicted_data.append({"DateTime": current_time_local})
    # print(f"Current_time: {current_time}")
    # print('Real time data from sensor for pm2.5 prediction')

    # print(selected_real_time_data_pm25)

    # print("===========================================================")
    model_pm25, rmse, mae, r2 = pm25_pred_model()
    predicted_data.append({"Pm25_RMSE": "{:.2f}".format(rmse)})
    predicted_data.append({"Pm25_MAE": "{:.2f}".format(mae)})
    predicted_data.append({"Pm25_R2": "{:.2f}".format(r2)})
    pm25_prediction = model_pm25
    prediction_pm25 = pm25_prediction.predict(selected_real_time_data_pm25)
    extracted_value = prediction_pm25[0]
    predicted_data.append({"Pm25_Pred": extracted_value})

    # print(f"Predicted Pm25: {prediction_pm25}")

    # print("===========================================================")

    return extracted_value

# Example usage of prediction function
# print(temp_test_prediction())
# print(humid_test_prediction())
# print(co2_test_prediction())
# print(voc_test_prediction())
# print(pm25_test_prediction())
# print(f"Predicted Temperature: {predicted_data}")
