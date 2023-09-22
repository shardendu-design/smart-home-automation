# import nec
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import json
import csv
import matplotlib.pyplot as plt
import seaborn as sns

awair_csv_data = pd.read_csv("awair_01-03-23_work_room.csv")
awair_csv_data.dtypes
awair_csv_data.head()
selected_required_columns = awair_csv_data[['timestamp','temp','humid','co2','voc','pm25','location']]
selected_required_columns.head()
selected_required_columns['timestamp'] = pd.to_datetime(selected_required_columns['timestamp']).dt.strftime('%d/%m/%Y %H:%M')
selected_required_columns
selected_required_columns.rename(columns = {'timestamp':'DateTime', 'temp':'Temp',
                              'humid':'Humid', 'co2':'Co2', 'voc':'Voc', 'pm25':'Pm25', 'location':'Location'},
                                 inplace = True)
selected_required_columns
# check data type
print(selected_required_columns.dtypes)
# Check for missing values
print(selected_required_columns.isna().sum())
# Check for duplicate rows
print(selected_required_columns.duplicated().sum())
# Drop duplicate rows
selected_required_columns = selected_required_columns.drop_duplicates()
selected_required_columns
# Calculate summary statistics
summary_stats = selected_required_columns.describe()
summary_stats
# Visualize temperature and CO2 levels using scatter plot
plt.figure(figsize=(8,5))
plt.scatter(selected_required_columns['Temp'], selected_required_columns['Co2'])
plt.xlabel('Temperature')
plt.ylabel('CO2 Levels')
plt.title('Temperature vs. CO2 Levels')

plt.show()

# Calculate correlation between temperature and humidity
correlation = selected_required_columns['Temp'].corr(selected_required_columns['Humid'])
correlation
# Create a histogram of PM2.5 levels
plt.hist(selected_required_columns['Pm25'], bins=10)
plt.xlabel('PM2.5 Levels')
plt.ylabel('Frequency')
plt.title('Distribution of PM2.5 Levels')
plt.show()

# Create a histogram of Humidity levels
plt.hist(selected_required_columns['Humid'], bins=10)
plt.xlabel('Humidity Levels')
plt.ylabel('Frequency')
plt.title('Distribution of Humidity Levels')
plt.show()

# Create a histogram of Humidity levels
plt.hist(selected_required_columns['Co2'], bins=10)
plt.xlabel('Co2 Levels')
plt.ylabel('Frequency')
plt.title('Distribution of Co2 Levels')
plt.show()

# Create a histogram of Humidity levels
plt.hist(selected_required_columns['Voc'], bins=10)
plt.xlabel('Voc Levels')
plt.ylabel('Frequency')
plt.title('Distribution of Voc Levels')
plt.show()

correlation_matrix = selected_required_columns.corr()
print(correlation_matrix)

plt.figure(figsize=(8,5))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')

plt.figure(figsize=(8,5))
selected_required_columns.plot(x='Temp', y='Humid', kind='scatter')
plt.xlabel('Temp')
plt.ylabel('Humid')
plt.title('Relationship between Temprature and Humidity')
plt.show()

awair_csv_data_new = pd.read_csv("1awair_data.csv")
awair_csv_data_new

awair_csv_data_new.dtypes
selected_required_columns_new = awair_csv_data_new[['timestamp','temp','humid','co2','voc','pm25','location']]
selected_required_columns_new['timestamp'] = pd.to_datetime(selected_required_columns_new['timestamp']).dt.strftime('%d/%m/%Y %H:%M')
selected_required_columns_new
print(selected_required_columns_new.dtypes)
# Check for missing values
print(selected_required_columns_new.isna().sum())

# Check for duplicate rows
print(selected_required_columns_new.duplicated().sum())

# Calculate summary statistics
summary_stats_new = selected_required_columns_new.describe()
summary_stats_new

# Create a histogram of PM2.5 levels
plt.hist(selected_required_columns_new['pm25'], bins=10)
plt.xlabel('PM2.5 Levels')
plt.ylabel('Frequency')
plt.title('Distribution of PM2.5 Levels')
plt.show()

# Create a histogram of Humidity levels
plt.hist(selected_required_columns_new['humid'], bins=10)
plt.xlabel('Humidity Levels')
plt.ylabel('Frequency')
plt.title('Distribution of Humidity Levels')
plt.show()

# Create a histogram of Humidity levels
plt.hist(selected_required_columns_new['voc'], bins=10)
plt.xlabel('Voc Levels')
plt.ylabel('Frequency')
plt.title('Distribution of Voc Levels')
plt.show()

# Create a histogram of Humidity levels
plt.hist(selected_required_columns_new['co2'], bins=10)
plt.xlabel('Co2 Levels')
plt.ylabel('Frequency')
plt.title('Distribution of Co2 Levels')
plt.show()
