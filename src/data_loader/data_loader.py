# Data loading and preprocessing

import pandas as pd
import os
import csv
import time
current_directory = os.path.dirname(os.path.abspath(__file__))


def data_preprocessing():
        while True:
        
            # Load the collected data into a DataFrame
            
           
            awair_csv_data = pd.read_csv("/media/shardendujha/backup1/Awair_Data/awair_data.csv")
            
            

            selected_required_columns = awair_csv_data[['temp', 'humid', 'co2', 'voc', 'pm25']]
            selected_required_columns = selected_required_columns.dropna()
            selected_required_columns = selected_required_columns.drop_duplicates()
            
            
            
            

            csv_file = "/media/shardendujha/backup1/processed_data/processed_data.csv" 
            if os.path.isfile(csv_file):
                # Load the existing data to check for duplicates
                existing_data = pd.read_csv(csv_file)

                # Concatenate the existing data and new data
                combined_data = pd.concat([existing_data, selected_required_columns])

                # Drop duplicates based on all columns
                combined_data = combined_data.drop_duplicates()

                # Save the combined data to the CSV file
                combined_data.to_csv(csv_file, index=False)
            else:
                try:
                    # Create a new CSV file without a header if it doesn't exist
                    selected_required_columns.to_csv(csv_file, header=True, index=False)
                except ValueError:
                    print("I/O error")
            
            time.sleep(300)




# if __name__ == '__main__':
#     data_preprocessing()

