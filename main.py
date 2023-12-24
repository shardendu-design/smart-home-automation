from src.sensor_api import sensor_api_connection
from src.models import model_test_with_live_data
from src.data_loader import data_loader
from src.air_cooler_integration import air_cooler
from src.WiFi_Socket import tapo_info
from src.current_weather_outdoor import current_weather_outside
import threading
import time
import psycopg2
import csv
import os
import pandas as pd
import datetime
from tabulate import tabulate


host = os.environ.get('CONTAINER_IP')
port = os.environ.get('PORT')
database = os.environ.get('DATABASE')
user = os.environ.get('USER')
password = os.environ.get('PASS_WORD')

predicted_csv = os.environ.get('predicted_data')

def outside_weather_now():
    while True:
        current_weather_outside.outdoor_weather()

def awair_row_data():
    while True:

        sensor_api_connection.awair_api_call()
        

def data_preprocess():
    while True:

        data_loader.data_preprocessing()

def model_execution_with_live_data():
    while True:

        model_test_with_live_data.temp_test_prediction()
        
        model_test_with_live_data.humid_test_prediction()
        
        model_test_with_live_data.co2_test_prediction()
        
        model_test_with_live_data.voc_test_prediction()
        
        model_test_with_live_data.pm25_test_prediction()
        
        predicted_values = model_test_with_live_data.predicted_data

        
        pred_temp_value = predicted_values[2]
        pred_temp_humid = predicted_values[5]
        pred_temp_co2 = predicted_values[8]
        pred_temp_voc = predicted_values[11]
        predicted_temp_pm25 = predicted_values[14]
        
        pred_temp_value_only = []
        for k,temp in pred_temp_value.items():
            pred_temp_value_only.append(round(temp, 2))

        pred_humid_value_only = []

        for k,humid in pred_temp_humid.items():
            pred_humid_value_only.append(round(humid, 2))

        pred_co2_value_only = []

        for k,co2 in pred_temp_co2.items():
            pred_co2_value_only.append(co2)
        
        pred_voc_value_only = []
        for k,voc in pred_temp_voc.items():
            pred_voc_value_only.append(voc)

        pred_pm25_value_only = []

        for k,pm25 in predicted_temp_pm25.items():
            pred_pm25_value_only.append(pm25)

        headers = ['Predicted Temperature','Predicted Humidity','Predicted Co2','Predicted Voc','Predicted Pm25']
        zipped_values = list(zip(pred_temp_value_only,pred_humid_value_only,pred_co2_value_only,pred_voc_value_only,pred_pm25_value_only))
        print('')
        print('                                     Predicted Parameters')
        print(tabulate(zipped_values , headers=headers, tablefmt='pretty'))
        # # print(temp,humid)


        air_cooler.air_coller_integration(temp,humid)

        
        conn1 = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
         
        )

        conn1.autocommit=True

        cur1 = conn1.cursor()
        cur1.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'awair'")
        exists = cur1.fetchone()

        if not exists:
            cur1.execute("CREATE DATABASE awair")

        conn1.set_session(autocommit=True)

        try:

            conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
            )
        except psycopg2.Error as e:
            print(e)

        try:
            cur = conn.cursor()
        except psycopg2.Error as e:

            print("Error: Could not get the cursor to the database")
            print(e)

        conn.set_session(autocommit=True)

        try:
    
            cur.execute("CREATE TABLE IF NOT EXISTS predicted_data (id SERIAL PRIMARY KEY,\
                                            DateTime TIMESTAMP,\
                                            Temperature_Test_Score NUMERIC,\
                                            Temperature_Predicted_Value NUMERIC,\
                                            Humidity_Test_Score NUMERIC,\
                                            Humidity_Predicted_Value NUMERIC,\
                                            Co2_Test_Score NUMERIC,\
                                            Co2_Predicted_Value NUMERIC,\
                                            VOC_Test_Score NUMERIC,\
                                            VOC_Predicted_Value NUMERIC,\
                                            Pm25_Test_Score NUMERIC,\
                                            Pm25_Predicted_Value NUMERIC);")
        
        except psycopg2.Error as e:
            print("Error: Issue creating table")
            print(e)

        record = {}

        for item in predicted_values:
            key = list(item.keys())[0]
            value = item[key]
            record[key] = value

        columns = ', '.join(record.keys())
        placeholders = ', '.join(['%s'] * len(record))

        sql = f"INSERT INTO predicted_data ({columns}) VALUES ({placeholders})"

        try:
            cur.execute(sql, list(record.values()))
            conn.commit()
        except psycopg2.Error as e:
            print("Error:", e)
            conn.rollback()
       

        # save data as csv file
        
        csv_file = predicted_csv 
        # Merge dictionaries into a single dictionary
        merged_data = {}
        for item in predicted_values:
            merged_data.update(item)

        # Check if the file exists and write data accordingly
        with open(csv_file, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=merged_data.keys())
            if csvfile.tell() == 0:  # If the file is empty, write header
                writer.writeheader()
            writer.writerow(merged_data)
        
        
        
        time.sleep(600)
                
def energy_consumption():
    while True:
        tapo_info.energy_time_calculation()
    
if __name__ == '__main__':
    
    import concurrent.futures
    import warnings

    def suppress_warnings():
        warnings.filterwarnings(action='ignore', category=UserWarning, module='sklearn')

    # Call suppress_warnings() before executing the functions that trigger the warnings
    suppress_warnings()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit both functions for execution
        current_weather = executor.submit(outside_weather_now)
        api_row_data = executor.submit(awair_row_data)
        future_data = executor.submit(data_preprocess)
        future_model = executor.submit(model_execution_with_live_data)
        energy_data = executor.submit(energy_consumption)
       
        # Wait for both functions to complete
        concurrent.futures.wait([future_model, energy_data, api_row_data, future_data])
        
       

    







