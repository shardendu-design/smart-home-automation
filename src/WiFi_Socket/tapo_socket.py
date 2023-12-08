import json
import requests
import pandas as pd 

api_url = 'https://api.smartthings.com'
access_token = '6b887913-d689-4c1d-bb66-92a8734973c3'

# Example endpoint to get devices
devices_endpoint = '/v1/devices'

headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

# Make a GET request to retrieve devices
response = requests.get(api_url + devices_endpoint, headers=headers)
plug_info = []
if response.status_code == 200:
    devices = response.json()
    plug_info.append(devices)
   
    # print(devices)
    # Process devices data here
else:
    print(f"Failed to retrieve devices. Status code: {response.status_code}")


# # Iterate through each dictionary in the list
# for data_dict in plug_info:
#     # Access the 'items' key which contains a list of items
#     items_list = data_dict.get('items', [])

#     # Iterate through each item in the 'items' list
#     for item in items_list:
#         print(f"Device ID: {item['deviceId']}")
#         print(f"Name: {item['name']}")
#         print(f"Label: {item['label']}")
#         print(f"Manufacturer Name: {item['manufacturerName']}")
#         print(f"Type: {item['type']}")
#         print(f"Create Time: {item['createTime']}")
#         print("\n")

#         # Access and print nested attributes
#         for component in item['components']:
#             print(f"Component ID: {component['id']}")
#             print(f"Component Label: {component['label']}")

#             for capability in component['capabilities']:
#                 print(f"Capability ID: {capability['id']}")
#                 print(f"Capability Version: {capability['version']}")

#             for category in component['categories']:
#                 print(f"Category Name: {category['name']}")
#                 print(f"Category Type: {category['categoryType']}")

#         # Print viper info
#         viper_info = item['viper']
#         print(f"Viper Info:")
#         print(f"Unique Identifier: {viper_info['uniqueIdentifier']}")
#         print(f"Viper Manufacturer: {viper_info['manufacturerName']}")
#         print(f"Model Name: {viper_info['modelName']}")
#         print(f"Software Version: {viper_info['swVersion']}")
#         print(f"Hardware Version: {viper_info['hwVersion']}")
#         print(f"Endpoint App ID: {viper_info['endpointAppId']}")
#         print("\n")


def air_cooler_power_turn_on():

    api_url = 'https://api.smartthings.com'
    access_token = '6b887913-d689-4c1d-bb66-92a8734973c3'

    # Example endpoint to control a device (replace with the actual device ID)
    device_id = 'ffc95bcc-c1b0-49ff-9a8f-bdbfd919dedc'
    control_endpoint = f'/v1/devices/{device_id}/commands'

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # Payload to turn on the device
    payload = {
        'commands': [
            {
                'component': 'main',
                'capability': 'switch',
                'command': 'on'
            }
        ]
    }

    # Make a POST request to turn on the device
    response = requests.post(api_url + control_endpoint, json=payload, headers=headers)

    if response.status_code == 200:
        print("Device turned on successfully!")
    else:
        print(f"Failed to turn on the device. Status code: {response.status_code}")



def air_cooler_power_turn_off():

    api_url = 'https://api.smartthings.com'
    access_token = '6b887913-d689-4c1d-bb66-92a8734973c3'

    # Example endpoint to control a device (replace with the actual device ID)
    device_id = 'ffc95bcc-c1b0-49ff-9a8f-bdbfd919dedc'
    control_endpoint = f'/v1/devices/{device_id}/commands'

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # Payload to turn off the device
    payload = {
        'commands': [
            {
                'component': 'main',
                'capability': 'switch',
                'command': 'off'
            }
        ]
    }

    # Make a POST request to turn off the device
    response = requests.post(api_url + control_endpoint, json=payload, headers=headers)

    if response.status_code == 200:
        print("Device turned off successfully!")
    else:
        print(f"Failed to turn off the device. Status code: {response.status_code}")

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


def is_air_cooler_power_on():

    # Usage: Call the function with your access token and device ID to check the status
    access_token = '6b887913-d689-4c1d-bb66-92a8734973c3'
    device_id = 'ffc95bcc-c1b0-49ff-9a8f-bdbfd919dedc'

    status = check_device_status(access_token, device_id)
    if status is not None:
        pass
        # print("Device status:", status)

    # Accessing switch status value
    switch_status = status['components']['main']['switch']['switch']['value']

    # Printing the switch status
    # print("Switch status:", switch_status)

    if switch_status == "on":
        return True
    else:
        return False




