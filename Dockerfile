#Use an official Python runtime as a parent image with GPU support
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install FFmpeg
RUN apt-get -y update && \
    apt-get -y upgrade && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*


# Install any needed packages specified in requirements.txt
RUN pip install  -r requirements.txt

#Expose the port the app runs on
EXPOSE 5001

# Define environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]