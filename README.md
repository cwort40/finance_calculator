# Financial Calculators App

This is a Python Flask web application that provides financial calculators for options pricing and portfolio risk analysis.

## Features

- User authentication via Google OAuth
- Black-Scholes options pricing calculator
- Portfolio risk analysis calculator 
- Save calculation history to DynamoDB
- REST API endpoints for calculators

## Usage

### Local Development

1. Clone the repo
2. Install dependencies
3. Set environment variables
4. Run the app
5. Navigate to `http://localhost:5000`

### Docker Deployment 

A Dockerfile is included for containerization and deployment.


## Technologies Used

- Python
- Flask
- DynamoDB
- Yahoo Finance API
- Pandas
- Docker
- Gunicorn
- Google OAuth
