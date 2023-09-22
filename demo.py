import psycopg2

# Define the connection parameters
db_params = {
    'database': 'your_database_name',
    'user': 'your_username',
    'password': 'your_password',
    'host': 'localhost',  # Replace with the IP or hostname of your Raspberry Pi
    'port': '5432',       # Default PostgreSQL port
}

# Establish a connection
try:
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()

    # Now you can execute SQL queries and store data in PostgreSQL

    # Remember to commit your changes and close the connection when done
    connection.commit()
    connection.close()

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL:", error)

#Store Data on External Hard Drive:
external_drive_path = '/path/to/external/hard/drive/'
file_name = 'data.txt'

with open(external_drive_path + file_name, 'w') as file:
    file.write('Your data goes here')
