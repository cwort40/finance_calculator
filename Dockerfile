# Use a base image with Python 3.8
FROM python:3.8

# Set the working directory inside the container
WORKDIR /flaskProject

# Copy the requirements.txt into the container and install dependencies
COPY requirements.txt /flaskProject/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application into the container
COPY . /flaskProject

# Expose the port the app runs on
EXPOSE 5000

# Commented out line to run on development server
CMD ["python", "app/__init__.py"]

