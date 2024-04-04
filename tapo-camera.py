import json
import requests
import pandas as pd 
import psycopg2
import os

host = os.environ.get('CONTAINER_IP')
port = os.environ.get('PORT')
database = os.environ.get('DATABASE')
user = os.environ.get('USER')
password = os.environ.get('PASS_WORD')

smartthings_url = os.environ.get('smart_things_url')
accesstoken_smarttings = os.environ.get('access_token_smartthings')
# deviceendpoint_smartthings = os.environ.get('device_endpoint_smartthings')
deviceid = os.environ.get('device_id')

api_url = smartthings_url
access_token = accesstoken_smarttings

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

print(plug_info)