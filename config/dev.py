import os

host = os.environ.get('CONTAINER_IP')
port = os.environ.get('PORT')
database = os.environ.get('DATABASE')
user = os.environ.get('USER')
password = os.environ.get('PASS_WORD')

# host = os.environ.get('HOST') 
# port = os.environ.get('PORT') 
# database = os.environ.get('DATABASE') 
# user = os.environ.get('USER') 
# password = os.environ.get('PASSWORD') 

DEBUG = True
SECRET_KEY = password
SQLALCHEMY_DATABASE_URI = f"postgresql://{user}:{password}@{host}:{port}/{database}"
SQLALCHEMY_TRACK_MODIFICATIONS = False