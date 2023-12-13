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

predicted_data = []

def live_sensor_data():

    sensor_data = []
    Url = 'http://192.168.0.104/air-data/latest' # api url path
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

    # print("===========================================================")
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    predicted_data.append({"DateTime": current_time})
    # print(f"Current_time: {current_time}")
    # print('sensor_data')

    # print(selected_real_time_data)

    # print("===========================================================")

    # Predict temperature for new data
    model_temp, score = temp_pred_model()
    predicted_data.append({"Temperature_Test_Score": score})
    temp_prediction = model_temp
    

    prediction_temperature = temp_prediction.predict(selected_real_time_data)
    extracted_value = prediction_temperature[0]
    predicted_data.append({"Temperature_Predicted_Value": extracted_value})
    # print(f"predicted_temperature: {extracted_value}")

    # print("===========================================================")
    return extracted_value

# print(predicted_data)
def humid_test_prediction():

    # Predict humidity for new data
    df1 = pd.DataFrame(live_sensor_data())
    selected_real_time_data_humid = df1[['temp','co2','voc','pm25']]

    selected_real_time_data_humid = selected_real_time_data_humid.dropna()
    selected_real_time_data_humid = selected_real_time_data_humid.drop_duplicates()

    # print("===========================================================")
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    predicted_data.append({"DateTime": current_time})
    # print(f"Current_time: {current_time}")
    # print('Real time data from sensor for humidity prediction')

    # print(selected_real_time_data_humid)

    # print("===========================================================")
    model_humid, score = humid_pred_model()
    predicted_data.append({"Humidity_Test_Score": score})
    humid_prediction = model_humid
    prediction_humid = humid_prediction.predict(selected_real_time_data_humid)
    extracted_value = prediction_humid[0]
    predicted_data.append({"Humidity_Predicted_Value": extracted_value})

    # print(f"Predicted humidity: {prediction_humid}")

    # print("===========================================================")
    return extracted_value

def co2_test_prediction():

    # Predict Co2 for new data

    df2 = pd.DataFrame(live_sensor_data())
    selected_real_time_data_co2 = df2[['temp','humid','voc','pm25']]

    selected_real_time_data_co2 = selected_real_time_data_co2.dropna()
    selected_real_time_data_co2 = selected_real_time_data_co2.drop_duplicates()
    # print("===========================================================")
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    predicted_data.append({"DateTime": current_time})
    # print(f"Current_time: {current_time}")
    # print('Real time data from sensor for co2 prediction')

    # print(selected_real_time_data_co2)

    # print("===========================================================")
    model_co2, mse = co2_pred_model()
    predicted_data.append({"Co2_Test_Score": mse})
    co2_prediction = model_co2
    prediction_co2 = co2_prediction.predict(selected_real_time_data_co2)
    extracted_value = prediction_co2[0]
    predicted_data.append({"Co2_Predicted_Value": extracted_value})

    # print(f"Predicted co2: {prediction_co2}")

    # print("===========================================================")
    return extracted_value


def voc_test_prediction():

    # predict voc for new data

    df3 = pd.DataFrame(live_sensor_data())
    selected_real_time_data_voc = df3[['temp','humid','co2','pm25']]

    selected_real_time_data_voc = selected_real_time_data_voc.dropna()
    selected_real_time_data_voc = selected_real_time_data_voc.drop_duplicates()
    # print("===========================================================")
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    predicted_data.append({"DateTime": current_time})
    # print(f"Current_time: {current_time}")
    # print('Real time data from sensor for voc prediction')

    # print(selected_real_time_data_voc)

    # print("===========================================================")
    model_voc, mse = voc_pred_model()
    predicted_data.append({"VOC_Test_Score": mse})
    voc_prediction = model_voc
    prediction_voc = voc_prediction.predict(selected_real_time_data_voc)
    extracted_value = prediction_voc[0]
    predicted_data.append({"VOC_Predicted_Value": extracted_value})

    # print(f"Predicted voc: {prediction_voc}")

    # print("===========================================================")
    return extracted_value 

def pm25_test_prediction():

    # predict pm25 for new data

    df4 = pd.DataFrame(live_sensor_data())
    selected_real_time_data_pm25 = df4[['temp','humid','co2','voc']]

    selected_real_time_data_pm25 = selected_real_time_data_pm25.dropna()
    selected_real_time_data_pm25 = selected_real_time_data_pm25.drop_duplicates()
    # print("===========================================================")
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    predicted_data.append({"DateTime": current_time})
    # print(f"Current_time: {current_time}")
    # print('Real time data from sensor for pm2.5 prediction')

    # print(selected_real_time_data_pm25)

    # print("===========================================================")
    model_pm25, mse = pm25_pred_model()
    predicted_data.append({"Pm25_Test_Score": mse})
    pm25_prediction = model_pm25
    prediction_pm25 = pm25_prediction.predict(selected_real_time_data_pm25)
    extracted_value = prediction_pm25[0]
    predicted_data.append({"Pm25_Predicted_Value": extracted_value})

    # print(f"Predicted Pm25: {prediction_pm25}")

    # print("===========================================================")

    return extracted_value

