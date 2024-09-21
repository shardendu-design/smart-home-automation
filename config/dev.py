import os

host = os.environ.get('CONTAINER_IP')
port = os.environ.get('PORT')
database = os.environ.get('DATABASE')
user = os.environ.get('USER')
password = os.environ.get('PASS_WORD')



DEBUG = True

SECRET_KEY = os.urandom(24)

# SQLALCHEMY_DATABASE_URI = 'postgresql://shardendu:computer@localhost:5432/awair'

SQLALCHEMY_DATABASE_URI = f"postgresql://{user}:{password}@{host}:{port}/{database}"
SQLALCHEMY_TRACK_MODIFICATIONS = False