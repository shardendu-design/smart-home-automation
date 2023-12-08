from datetime import datetime
import requests
import time
import os
import csv 

def check_device_status(access_token, device_id):
    api_url = 'https://api.smartthings.com'
    status_endpoint = f'/v1/devices/{device_id}/status'

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # Make a GET request to retrieve device status
    response = requests.get(api_url + status_endpoint, headers=headers)

    if response.status_code == 200:
        device_status = response.json()
        return device_status
    else:
        print(f"Failed to get device status. Status code: {response.status_code}")
        return None
    
def calculate_total_used_time(time_data):
    start_times = []
    end_times = []
    
    for entry in time_data:
        if 'start_time' in entry:
            start_times.append(datetime.strptime(entry['start_time'], '%Y-%m-%dT%H:%M:%S.%fZ'))
        elif 'end_time' in entry:
            end_times.append(datetime.strptime(entry['end_time'], '%Y-%m-%dT%H:%M:%S.%fZ'))

    total_used_time = 0
    paired_times = zip(sorted(start_times), sorted(end_times))
    for start_time, end_time in paired_times:
        total_used_time += (end_time - start_time).total_seconds()
        
    return total_used_time



def energy_time_calculation():
    while True:


        # Usage: Call the function with your access token and device ID to check the status
        access_token = '6b887913-d689-4c1d-bb66-92a8734973c3'
        device_id = 'ffc95bcc-c1b0-49ff-9a8f-bdbfd919dedc'

        status = check_device_status(access_token, device_id)
        if status is not None:
            pass
            # print("Device status:", status)

        # Accessing switch status value
        switch_status = status['components']['main']['switch']['switch']['value']
        switch_timestamp = status['components']['main']['switch']['switch']['timestamp']
        # Printing the switch status
        # print("Switch status:", switch_status)
        # print("Switch timestamp:", switch_timestamp)

        s_columns = ['start_time']
        e_columns = ['end_time']
        start_times = []
        end_times = []
        if switch_status == "on":
            start_on_timestamp = switch_timestamp
            start_times.append(start_on_timestamp)
            csv_file = "/media/shardendujha/backup1/energy_cal_data/start_time_data.csv"
            path = "/media/shardendujha/backup1/energy_cal_data/start_time_data.csv"
            

            if os.path.exists(path):
                with open(csv_file, "a+") as add_obj:
                    writer = csv.DictWriter(add_obj, fieldnames=s_columns)
                    file_content = open(csv_file).read()
                    for data in start_times:
                        if data not in file_content:
                            writer.writerow({'start_time': data})
            else:
                try:
                    with open(csv_file, "w") as awair_file:
                        writer = csv.DictWriter(awair_file, fieldnames=s_columns)
                        writer.writeheader()
                        
                        for data in start_times:
                            writer.writerow({'start_time': data})
                            
                except ValueError:
                    print("I/O error")

            
        elif switch_status == "off":
            start_of_timestamp = switch_timestamp
            end_times.append(start_of_timestamp)
            csv_file = "/media/shardendujha/backup1/energy_cal_data/end_time_data.csv"
            path = "/media/shardendujha/backup1/energy_cal_data/end_time_data.csv"
           

            if os.path.exists(path):
                with open(csv_file, "a+") as add_obj:
                    writer = csv.DictWriter(add_obj, fieldnames=e_columns)

                    file_content = open(csv_file).read()
                    
                    for data in end_times:
                        if data not in file_content:
                            writer.writerow({'end_time': data})
            else:
                try:
                    with open(csv_file, "w") as awair_file:
                        writer = csv.DictWriter(awair_file, fieldnames=e_columns)
                        writer.writeheader()
                        
                        for data in end_times:
                            writer.writerow({'end_time': data})
                            
                except ValueError:
                    print("I/O error")
        else:
            print("Invalid timestamp")

        
        
        csv_file = "/media/shardendujha/backup1/energy_cal_data/end_time_data.csv"
        path = "/media/shardendujha/backup1/energy_cal_data/end_time_data.csv"

        merged_data = []

        if os.path.exists(path):
            with open(csv_file, 'r') as readfile:
                reader = csv.DictReader(readfile)

                for row in reader:
                    merged_data.append(row)

        csv_file = "/media/shardendujha/backup1/energy_cal_data/start_time_data.csv"
        path = "/media/shardendujha/backup1/energy_cal_data/start_time_data.csv"

        if os.path.exists(path):
            with open(csv_file, 'r') as readfile:
                reader = csv.DictReader(readfile)

                for row in reader:
                    merged_data.append(row)

        # print(merged_data)
        # total_used_time = calculate_total_used_time(merged_data)
        # print(f"The total used time is: {total_used_time} seconds")
        start_time_value = []
        end_time_vlaue = []
        for data in merged_data:
            for key, value in data.items():
                if key == 'start_time':
                    start_time_value.append(value)
                    
                if key == 'end_time':
                    end_time_vlaue.append(value)      

        electricity_cost_data = []

        for start, end in zip(start_time_value, end_time_vlaue):
            starttime = datetime.fromisoformat(start[:-1]) 
            endtime = datetime.fromisoformat(end[:-1])
            duration = (endtime - starttime).total_seconds() / 60
            # print(f"Start time: {starttime}, End time: {endtime}, Used time: {duration} minutes")

            device_capacity = 65 # in watts, device_consume_electricity
            min_in_hrs= round(duration/60,2) #calculate_total_min_in_hours_in_day
            watt_hours = round(device_capacity * min_in_hrs,2) # watt_hours_per_day
            kwh = round(watt_hours / 1000,2) # total_kwh_per_day
            price_per_kwh = 0.13 # 0.13 cents per hour,price_per_kwh
            e_tranf_cost = round(0.3 * kwh,2) # electricity_transfer_cost
            e_tax_cost = round(0.3 * kwh,2) # electricity_tax
            calculate_electricity_cost= price_per_kwh * kwh
            total_cost = round(calculate_electricity_cost + e_tranf_cost + e_tax_cost,2) # total_eletricity_cost
            electricity_cost_data = [{'Start_time': start,'End_time': end,
                                     'Used_time_hrs': min_in_hrs,
                                     'Price_per_kwh_cents': price_per_kwh,
                                     'Transfer_per_kwh': e_tranf_cost,
                                     'Tax_per_kwh': e_tax_cost,
                                     'Total_cost_euro': total_cost}]
            
            column_name  = ["Start_time", "End_time", "Used_time_hrs", "Price_per_kwh_cents",
                            "Transfer_per_kwh", "Tax_per_kwh", "Total_cost_euro"]
            
            csv_file = "/media/shardendujha/backup1/electricity_cost_analysis_data/cost_analysis_data.csv"
            path = "/media/shardendujha/backup1/electricity_cost_analysis_data/cost_analysis_data.csv"

            if os.path.exists(path):
                with open(csv_file, 'a+') as addfile:
                    writer = csv.DictWriter(addfile, fieldnames=column_name)

                    file_content = open(csv_file).read()
                    
                    for data in electricity_cost_data:
                        if f"{data['Start_time']},{data['End_time']}" not in file_content:
                            writer.writerow(data)

            else:
                try:
                    with open(csv_file, 'w') as writefile:
                        writer = csv.DictWriter(writefile, fieldnames=column_name)
                        writer.writeheader()
                        
                        
                        for data in electricity_cost_data:
                            writer.writerow(data)

                except ValueError:
                    print("I/O error")


            # print(electricity_cost_data)
            # print(f"Start time: {starttime}, End time: {endtime}, Used time: {duration} minutes")
        
        time.sleep(10)
        

# energy_time_calculation()     
