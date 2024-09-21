import psycopg2
import os

# Load environment variables
host = os.getenv('CONTAINER_IP', 'localhost')
port = os.getenv('PORT', 5432)
database = os.getenv('DATABASE', 'awair')
user = os.getenv('USER', 'shardendu')
password = os.getenv('PASS_WORD', 'computer')

# Connect to PostgreSQL
try:
    conn = psycopg2.connect(
        host=host,
        port=port,
        dbname=database,
        user=user,
        password=password
    )
    print("Connection successful!")
    conn.close()
except Exception as e:
    print(f"Error: {e}")
