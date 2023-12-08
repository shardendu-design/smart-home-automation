import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import requests
import time
import json # for access josn
import datetime # for tiemstamp
import csv # for acess csv
import psycopg2 # postgreSql connection
import threading
import os
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
# from tapo_plug import tapoPlugApi # this for wifi socket to maintain automation
import os
from email.message import EmailMessage # for email notification
import ssl # for security
import smtplib # SMTP client session
from sklearn.metrics import r2_score
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt

 
def real_time_data():
    
    while True:
        
        
    # Let's create multiple model to predict different parameters

    # model for temprature prediction 


        def temp_pred_model():


            # Load the collected data into a DataFrame
            awair_csv_data = pd.read_csv("/media/shardendujha/backup1/Awair_Data/awair_data.csv")

            selected_required_columns = awair_csv_data[['temp','humid','co2','voc','pm25']]
            selected_required_columns = selected_required_columns.dropna()
            selected_required_columns = selected_required_columns.drop_duplicates()

            # Split the data into input features (X) and target variable (y)
            X = selected_required_columns.drop('temp', axis=1)
            y = selected_required_columns ['temp']


            # Split the data into training and testing sets
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            # Initialize and train the linear regression model
            model_temp = LinearRegression()
            # # Fit the model on the training data
            model_temp.fit(X_train, y_train)
            #Make predictions using the trained model on the test set.

            y_pred = model_temp.predict(X_test)

            print(f"Y_pred : {y_pred}")
            # # Evaluate the model on the testing data
            score = model_temp.score(X_test, y_test)
            print('Test Score for temperature')
            print("===========================================================")
            print(f"R-squared score temperature: {score}")
            print("===========================================================")

            # Plotting the actual values
            plt.plot(y_test, label='Actual')
            # Plotting the predicted values
            plt.plot(y_pred, label='Predicted')
            # Adding labels and title to the plot
            plt.xlabel('Data Point')
            plt.ylabel('Temperature Value')
            plt.title('Actual vs Predicted temperature Values')
            # Adding legend
            plt.legend()
            # Display the plot
            plt.show()

            return model_temp

        def humid_pred_model():

            # Load the collected data into a DataFrame
            awair_csv_data = pd.read_csv("/media/shardendujha/backup1/Awair_Data/awair_data.csv")

            selected_required_columns = awair_csv_data[['temp','humid','co2','voc','pm25']]
            selected_required_columns = selected_required_columns.dropna()
            selected_required_columns = selected_required_columns.drop_duplicates()

            # Split the data into input features (X) and target variable (y)
            X = selected_required_columns.drop('humid', axis=1)
            y = selected_required_columns ['humid']


            # Split the data into training and testing sets
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            # Initialize and train the linear regression model
            model_humid = LinearRegression()
            # # Fit the model on the training data
            model_humid.fit(X_train, y_train)

            #Make predictions using the trained model on the test set.

            y_pred = model_humid.predict(X_test)

            print(f"Y_pred : {y_pred}")


            # # Evaluate the model on the testing data
            score = model_humid.score(X_test, y_test)
            print('Test Score for humidity')
            print("===========================================================")
            print(f"R-squared score humidity: {score}")
            print("===========================================================")

            # Plotting the actual values
            plt.plot(y_test, label='Actual')
            # Plotting the predicted values
            plt.plot(y_pred, label='Predicted')
            # Adding labels and title to the plot
            plt.xlabel('Data Point')
            plt.ylabel('Humidity Value')
            plt.title('Actual vs Predicted humid Values')
            # Adding legend
            plt.legend()
            # Display the plot
            plt.show()


            return model_humid

        def co2_pred_model():
            # Load the collected data into a DataFrame
            awair_csv_data = pd.read_csv("/media/shardendujha/backup1/Awair_Data/awair_data.csv")

            selected_required_columns = awair_csv_data[['temp','humid','co2','voc','pm25']]
            selected_required_columns = selected_required_columns.dropna()
            selected_required_columns = selected_required_columns.drop_duplicates()

            # Split the data into input features (X) and target variable (y)
            X = selected_required_columns.drop('co2', axis=1)
            y = selected_required_columns ['co2']


            # Split the data into training and testing sets
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            # Initialize and train the RandomForest model
            model_co2 = RandomForestRegressor(random_state=42)

            # # Fit the model on the training data
            model_co2.fit(X_train, y_train)

            #Make predictions using the trained model on the test set.

            y_pred = model_co2.predict(X_test)

            print(f"Y_pred : {y_pred}")

            # # Evaluate the model on the testing data
            mse = mean_squared_error(y_test, y_pred)
            print('Test Score for co2')
            print("===========================================================")
            print(f"Mean Squared Error co2: {mse}")
            print("===========================================================")

            # Plotting the actual values
            plt.plot(y_test, label='Actual')
            # Plotting the predicted values
            plt.plot(y_pred, label='Predicted')
            # Adding labels and title to the plot
            plt.xlabel('Data Point')
            plt.ylabel('CO2 Value')
            plt.title('Actual vs Predicted CO2 Values')
            # Adding legend
            plt.legend()

            # Display the plot
            plt.show()
            return model_co2

        def voc_pred_model():
            # Load the collected data into a DataFrame
            awair_csv_data = pd.read_csv("/media/shardendujha/backup1/Awair_Data/awair_data.csv")

            selected_required_columns = awair_csv_data[['temp','humid','co2','voc','pm25']]
            selected_required_columns = selected_required_columns.dropna()
            selected_required_columns = selected_required_columns.drop_duplicates()

            # Split the data into input features (X) and target variable (y)
            X = selected_required_columns.drop('voc', axis=1)
            y = selected_required_columns ['voc']


            # Split the data into training and testing sets
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            # Initialize and train the RandomForest model
            model_voc = RandomForestRegressor(random_state=42)
            # # Fit the model on the training data
            model_voc.fit(X_train, y_train)

            #Make predictions using the trained model on the test set.

            y_pred = model_voc.predict(X_test)

            print(f"Y_pred : {y_pred}")

            # # Evaluate the model on the testing data
            mse = mean_squared_error(y_test, y_pred)
            print('Test Score for voc')
            print("===========================================================")
            print(f"R-squared score voc: {mse}")
            print("===========================================================")

            # Plotting the actual values
            plt.plot(y_test, label='Actual')
            # Plotting the predicted values
            plt.plot(y_pred, label='Predicted')
            # Adding labels and title to the plot
            plt.xlabel('Data Point')
            plt.ylabel('VOC Value')
            plt.title('Actual vs Predicted voc Values')
            # Adding legend
            plt.legend()

            # Display the plot
            plt.show()

            return model_voc

        def pm25_pred_model():
            # Load the collected data into a DataFrame
            awair_csv_data = pd.read_csv("/media/shardendujha/backup1/Awair_Data/awair_data.csv")

            selected_required_columns = awair_csv_data[['temp','humid','co2','voc','pm25']]
            selected_required_columns = selected_required_columns.dropna()
            selected_required_columns = selected_required_columns.drop_duplicates()

            # Split the data into input features (X) and target variable (y)
            X = selected_required_columns.drop('pm25', axis=1)
            y = selected_required_columns ['pm25']


            # Split the data into training and testing sets
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            # Initialize and train the RandomForest model
            model_pm25 = RandomForestRegressor(random_state=42)
            # # Fit the model on the training data
            model_pm25.fit(X_train, y_train)

            #Make predictions using the trained model on the test set.

            y_pred = model_pm25.predict(X_test)

            print(f"Y_pred : {y_pred}")

            # # Evaluate the model on the testing data
            mse = mean_squared_error(y_test, y_pred)
            print('Test Score for pm25')
            print("===========================================================")
            print(f"R-squared score pm25: {mse}")
            print("===========================================================")

            # Plotting the actual values
            plt.plot(y_test, label='Actual')
            # Plotting the predicted values
            plt.plot(y_pred, label='Predicted')
            # Adding labels and title to the plot
            plt.xlabel('Data Point')
            plt.ylabel('PM2.5 Value')
            plt.title('Actual vs Predicted Pm2.5 Values')
            # Adding legend
            plt.legend()

            # Display the plot
            plt.show()

            return model_pm25

        # def air_cooler_power_turn_on():

        #     device = {
        #                 "tapoIp": "192.168.0.105",
        #                 "tapoEmail": "appujha0@gmail.com",
        #                 "tapoPassword": "Computer1234"
        #             }

        #     response = tapoPlugApi.plugOn(device)
        #     print(response)
        #     print('Air Cooler is Turned On Successfully')
        #     return response

        # def air_cooler_power_turn_off():

        #     device = {
        #             "tapoIp": "192.168.0.105",
        #             "tapoEmail": "appujha0@gmail.com",
        #             "tapoPassword": "Computer1234"
        #         }

        #     response = tapoPlugApi.plugOff(device)
        #     print(response)
        #     print('Air Cooler is Turned Off Successfully')
        #     return response

        # def send_email_notification_turn_on():

        #     email_sender = 'appujha0@gmail.com'
        #     email_password = os.environ.get('PASSWORD') # activate env,export PASSWORD=<password>,echo $PASSWORD

        #     email_receiver = 'appujha0@gmail.com'

        #     subject = 'awair sensor notification'
        #     body = """

        #                 subject: awair sensor temperature notification!


        #                 Your room temperature has exceed the threshold,and air cooler has turend on successfully.

        #                 Br,
        #                 Test Company.
        #                 Vantaa,Finland

        #                 """

        #     em = EmailMessage()
        #     em['From'] = email_sender 
        #     em['To'] = email_receiver
        #     em['Subject'] = subject
        #     em.set_content(body)

        #     context = ssl.create_default_context()

        #     with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        #         smtp.login(email_sender,email_password)
        #         smtp.sendmail(email_sender,email_receiver,em.as_string())  # Send email


        # def send_email_notification_turn_off():

        #     email_sender = 'appujha0@gmail.com'
        #     email_password = 'Computer@520192' ##### os.environ.get('PASSWORD')

        #     email_receiver = 'appujha0@gmail.com'

        #     subject = 'awair sensor notification'
        #     body = """

        #                 subject: Awair sensor temperature notification!


        #                 Your room temperature has exceed the threshold,and air cooler has turend off successfully.

        #                 Br,
        #                 Test Company.
        #                 Vantaa,Finland

        #                 """

        #     em = EmailMessage()
        #     em['From'] = email_sender 
        #     em['To'] = email_receiver
        #     em['Subject'] = subject
        #     em.set_content(body)

        #     context = ssl.create_default_context()

        #     with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        #         smtp.login(email_sender,email_password)
        #         smtp.sendmail(email_sender,email_receiver,em.as_string())  # Send email


        # def is_air_cooler_power_on():
        #     device = {
        #         "tapoIp": "192.168.0.105",
        #         "tapoEmail": "appujha0@gmail.com",
        #         "tapoPassword": "Computer1234"
        #     }

        #     response = tapoPlugApi.getDeviceInfo(device)

        #     # Parse the JSON data
        #     parsed_data = json.loads(response)
        #     # Store key-value pairs in a list
        #     key_value_pairs = list(parsed_data.items())

        #     # Print the key-value pairs
        #     plug_info = []
        #     for key, value in key_value_pairs:
        #         plug_info.append(value)

        #     plug_data = plug_info[0]

        #     power_status = plug_data['device_on']

        #     if power_status == True:
        #         return True
        #     else:
        #         return False





       
        prev_temperature = None  # Variable to store previous temperature value
        prev_humidity = None



        sensor_data = []

        Url = 'http://192.168.0.104/air-data/latest' # api url path
        request = requests.request("GET", Url)
        data = request.json()
        add_new_col = {'location':'Janonhanta1,Vantaa,Finland'}

        add_bew_col_serial = {}
        data.update(add_bew_col_serial)
        data.update(add_new_col)
        sensor_data.append(data)



        df = pd.DataFrame(sensor_data)
        selected_real_time_data = df[['humid','co2','voc','pm25']]

        selected_real_time_data = selected_real_time_data.dropna()
        selected_real_time_data = selected_real_time_data.drop_duplicates()

        print("===========================================================")
        current_time = datetime.datetime.now()
        print(f"Current_time: {current_time}")
        print('Real time data from sensor for temprature ptrediction')

        print(selected_real_time_data)

        print("===========================================================")

        # Predict temperature for new data
        temp_prediction = temp_pred_model()
        prediction_temperature = temp_prediction.predict(selected_real_time_data)

        print(f"Predicted temperature: {prediction_temperature}")

        print("===========================================================")






        # Predict humidity for new data
        df1 = pd.DataFrame(sensor_data)
        selected_real_time_data_humid = df1[['temp','co2','voc','pm25']]

        selected_real_time_data_humid = selected_real_time_data_humid.dropna()
        selected_real_time_data_humid = selected_real_time_data_humid.drop_duplicates()

        print("===========================================================")
        current_time = datetime.datetime.now()
        print(f"Current_time: {current_time}")
        print('Real time data from sensor for humidity prediction')

        print(selected_real_time_data_humid)

        print("===========================================================")

        humid_prediction = humid_pred_model()
        prediction_humid = humid_prediction.predict(selected_real_time_data_humid)

        print(f"Predicted humidity: {prediction_humid}")

        print("===========================================================")


        # Predict Co2 for new data

        df2 = pd.DataFrame(sensor_data)
        selected_real_time_data_co2 = df1[['temp','humid','voc','pm25']]

        selected_real_time_data_co2 = selected_real_time_data_co2.dropna()
        selected_real_time_data_co2 = selected_real_time_data_co2.drop_duplicates()
        print("===========================================================")
        current_time = datetime.datetime.now()
        print(f"Current_time: {current_time}")
        print('Real time data from sensor for co2 prediction')

        print(selected_real_time_data_co2)

        print("===========================================================")

        co2_prediction = co2_pred_model()
        prediction_co2 = co2_prediction.predict(selected_real_time_data_co2)

        print(f"Predicted co2: {prediction_co2}")

        print("===========================================================")




        # predict voc for new data

        df3 = pd.DataFrame(sensor_data)
        selected_real_time_data_voc = df3[['temp','humid','co2','pm25']]

        selected_real_time_data_voc = selected_real_time_data_voc.dropna()
        selected_real_time_data_voc = selected_real_time_data_voc.drop_duplicates()
        print("===========================================================")
        current_time = datetime.datetime.now()
        print(f"Current_time: {current_time}")
        print('Real time data from sensor for voc prediction')

        print(selected_real_time_data_voc)

        print("===========================================================")

        voc_prediction = voc_pred_model()
        prediction_voc = voc_prediction.predict(selected_real_time_data_voc)

        print(f"Predicted voc: {prediction_voc}")

        print("===========================================================")


        # predict pm25 for new data

        df4 = pd.DataFrame(sensor_data)
        selected_real_time_data_pm25 = df4[['temp','humid','co2','voc']]

        selected_real_time_data_pm25 = selected_real_time_data_pm25.dropna()
        selected_real_time_data_pm25 = selected_real_time_data_pm25.drop_duplicates()
        print("===========================================================")
        current_time = datetime.datetime.now()
        print(f"Current_time: {current_time}")
        print('Real time data from sensor for pm2.5 prediction')

        print(selected_real_time_data_pm25)

        print("===========================================================")

        pm25_prediction = pm25_pred_model()
        prediction_pm25 = pm25_prediction.predict(selected_real_time_data_pm25)

        print(f"Predicted Pm25: {prediction_pm25}")

        print("===========================================================")




        # # Integrate with the wifi socket based on the predicted values

        # if prediction_temperature >= 22 or prediction_humid <= 40:
        #     if (prev_temperature is None or prediction_temperature != prev_temperature) or \
        #     (prev_humidity is None or prediction_humid != prev_humidity):
                
        #         if is_air_cooler_power_on()== False:
                
        #             air_cooler_power_turn_on()
                    

        #             send_email_notification_turn_on()

        #         prev_temperature = prediction_temperature
        #         prev_humidity = prediction_humid


        # else:
        #     if prev_temperature is None or prediction_temperature != prev_temperature:
        #         if is_air_cooler_power_on()==True:

        #             air_cooler_power_turn_off()

        #             send_email_notification_turn_off()

        #         prev_temperature = prediction_temperature
        #         prev_humidity = prediction_humid


        time.sleep(1200)# call every 5 min 


        
        
            
        
             
if __name__ == '__main__':
    real_time_data()
