from src.sensor_api import sensor_api_connection
from src.models import model_test_with_live_data
from src.data_loader import data_loader
import concurrent.futures
import threading
import time
import psycopg2
import csv
import json
import os
from src.air_cooler_integration import air_cooler
import pandas as pd
from src.WiFi_Socket import tapo_info
from tabulate import tabulate
import datetime

host = os.environ.get('CONTAINER_IP')
port = os.environ.get('PORT')
database = os.environ.get('DATABASE')
user = os.environ.get('USER')
password = os.environ.get('PASS_WORD')


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
        pred_temp_co2 = predicted_values[7]
        
        pred_temp_voc = predicted_values[9]
        
        pred_temp_pm25 = predicted_values[11]
        
        
        pred_temp_value_only = []
        for k,temp in pred_temp_value.items():
            pred_temp_value_only.append(temp)

        pred_humid_value_only = []

        for k,humid in pred_temp_humid.items():
            pred_humid_value_only.append(humid)

        pred_co2_value_only = []

        for k,co2 in pred_temp_co2.items():
            pred_co2_value_only.append(co2)

        pred_voc_value_only = []

        for k,voc in pred_temp_voc.items():
            pred_voc_value_only.append(voc)

        pred_temp_pm25_value_only = []

        for k,pm25 in pred_temp_pm25.items():
            pred_temp_pm25_value_only.append(pm25)

        

        headers = ['Predicted_Temp','Predicted_Humid','Predicted_Co2','Predicted_Voc','Predicted_pm25']
        data = list(zip(pred_temp_value_only, pred_humid_value_only,pred_co2_value_only,pred_voc_value_only,pred_temp_pm25_value_only))
        
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("                                       Predicted Values:")
        print("                                       Date and Time:", time_now)
        print("*" * 245)
        print(tabulate(data, headers, tablefmt='pretty'))

        
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
        
        csv_file = "/media/shardendujha/backup1/predicted_data/prediceted_data.csv" 
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
        
        
        
        time.sleep(300)
                
def energy_consumption():
    while True:
        tapo_info.energy_time_calculation()
    
if __name__ == '__main__':
    

    # Create a ThreadPoolExecutor to run the functions concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit both functions for execution
        api_row_data = executor.submit(awair_row_data)
        future_data = executor.submit(data_preprocess)
        future_model = executor.submit(model_execution_with_live_data)
        energy_data = executor.submit(energy_consumption)
       
        
        # Wait for both functions to complete
        concurrent.futures.wait([api_row_data,future_data,future_model,energy_data])
       

    







