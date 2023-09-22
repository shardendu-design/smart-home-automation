#Get plug time usage
import pandas as pd
from datetime import datetime, timedelta
from time import sleep
from datetime import date
from tapo_plug import tapoPlugApi
import time
import os
import csv
import json


def power_socket():
    
    while True:
        
    
        device = {
            "tapoIp": "192.168.1.100",
            "tapoEmail": "appujha0@gmail.com",
            "tapoPassword": "Computer1234"
        }
  
        response = tapoPlugApi.getPlugUsage(device)
        # print(response)

        # Parse the JSON string into a dictionary
        data = json.loads(response)

        plug_time = []
        

        # Iterate over the dictionary and retrieve each key-value pair
        for key, value in data.items():
            plug_time.append(value)
        #     print(key, ":", value)
    
        # print(plug_time[0])

        plug_usage_time_data = pd.DataFrame(plug_time[0])

        time_usage_in_min_last30_days  = plug_usage_time_data.iloc[0]
        time_usage_in_min_last7_days = plug_usage_time_data.iloc[1]
        time_usage_in_min_today = plug_usage_time_data.iloc[2]

        # print("Time used in last 30 days.",time_usage_in_min_last30_days)
        # print("Time used in last 7 days." ,time_usage_in_min_last7_days)
#         print("time used today", time_usage_in_min_today)
        
        usage_data = {}
        
        
        date_today = date.today()
        formatted_date = date_today.strftime("%d/%m/%Y")
    

        for r in time_usage_in_min_today:
            time_usage = r
            
            device_capacity = 65 # in watts, device_consume_electricity
            min_in_hrs= round(r/60,2) #calculate_total_min_in_hours_in_day
            watt_hours_day = round(device_capacity * min_in_hrs,2) # watt_hours_per_day
            kwh_day = round(watt_hours_day / 1000,2) # total_kwh_per_day
            price_per_kwh = 0.13 # 0.13 cents per hour,price_per_kwh
            e_tranf_cost = round(0.3 * kwh_day,2) # electricity_transfer_cost
            e_tax_cost = round(0.3 * kwh_day,2) # electricity_tax
            calculate_electricity_cost= price_per_kwh * kwh_day
            total_cost = round(calculate_electricity_cost + e_tranf_cost + e_tax_cost,2) # total_eletricity_cost
#             print("Device Capacity in watt", device_consume_electricity)
#             print("Total watt hours in a day",watt_hours_per_day)
#             print("Total kwh per day", total_kwh_per_day)
#             print("Price per kwh", price_per_kwh)
#             print("Electricity transfer cost in per kwh", electricity_transfer_cost)
#             print("Electricity Tax cost in per kwh", electricity_tax)
#             print("Total cost of the electricity in euro", total_eletricity_cost)
            

            columns = ["formatted_date","time_usage","device_capacity","min_in_hrs",\
                        "watt_hours_day","kwh_day","price_per_kwh", \
                        "e_tranf_cost","e_tax_cost","total_cost"]
            for row in columns:
                usage_data[row] = eval(row)

#             print(usage_data)
    
        # save data as csv file
        
       
        c_columns = ["formatted_date","time_usage","device_capacity","min_in_hrs",\
                        "watt_hours_day","kwh_day","price_per_kwh", \
                        "e_tranf_cost","e_tax_cost","total_cost"]
        csv_file = "/Volumes/backup1/Awair_Data/wifi_socket_usage_time__data.csv"
        path = "/Volumes/backup1/Awair_Data/wifi_socket_usage_time__data.csv"
        
        
           
        
        if os.path.exists(path):
            
            existing_file = pd.read_csv(csv_file)
            existing_data = existing_file['formatted_date']
            current_data = pd.Series(usage_data['formatted_date'])
    
            
            if current_data.isin(existing_data).any():
                
                print('Values from current_data exist in existing_data')
                
                    
            else:
                
                with open(csv_file, "a+", newline="") as file:
                    writer = csv.DictWriter(file, fieldnames=c_columns) 
                    writer.writerow(usage_data)

        
                       
        else:
            try:
                with open(csv_file, "w", newline="") as file:
                    writer = csv.DictWriter(file, fieldnames=c_columns)
                    writer.writeheader()
                    writer.writerow(usage_data)
                    
                         
            except IOError:
                print("I/O error occurred while writing the CSV file.")
                        
              
        interval_seconds = 24 * 60 * 60
        time.sleep(interval_seconds)



if __name__ == '__main__':
    power_socket()