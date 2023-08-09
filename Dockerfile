# Use a base image with Python 3.8
FROM python:3.8

# Set the working directory inside the container
WORKDIR /flaskProject

# Add app directory to the Python path
ENV PYTHONPATH /flaskProject/app:$PYTHONPATH

# Copy the requirements.txt into the container and install dependencies
COPY requirements.txt /flaskProject/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy the entire application into the container
COPY . /flaskProject

# Expose the port the app runs on
EXPOSE 5000

# Command to run gunicorn with the specified options
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app.__init__:app"]
