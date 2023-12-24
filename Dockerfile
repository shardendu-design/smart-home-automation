# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /Home_Automation

# Copy the current directory contents into the container at /app
COPY . /Home_Automation

# Install Python dependencies from requirements.txt
RUN pip install -r requirements.txt

# Define the command to run the application
CMD ["python", "main.py"]
