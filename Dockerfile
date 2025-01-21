# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /Home_Automation

# Copy the current directory contents into the container at /app
COPY app /Home_Automation/app
COPY src /Home_Automation/src
COPY app_main.py /Home_Automation/app_main.py
COPY config /Home_Automation/config
COPY main.py /Home_Automation/main.py
COPY seperate.py /Home_Automation/seperate.py

# Install Python dependencies from requirements.txt
COPY requirments.txt /Home_Automation/requirments.txt
RUN pip install -r requirements.txt

# Define the command to run the application
CMD ["python", "app_main.py"]
