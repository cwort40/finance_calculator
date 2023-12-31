import uuid
from datetime import datetime

import boto3
from flask import Blueprint, request, render_template, session

from blueprints.auth import login_required
from utils import portfolio_risk_analysis

from decimal import Decimal

from flask_limiter.util import get_remote_address
from flask_limiter import Limiter

portfolio_risk_limiter = Limiter(key_func=get_remote_address)

portfolio_risk_calculator = Blueprint('portfolio_risk_calculator', __name__, template_folder='../templates')

dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
table = dynamodb.Table('UserCalculations')


# Adding login_required decorator for now, will implement API auth tokens later
@portfolio_risk_calculator.route('/api/portfolio_risk_analysis', methods=['GET'])
@portfolio_risk_limiter.limit("10 per minute")
def api_calculate_portfolio_risk():
    try:
        stocks = request.args.get('stocks').split(',')
        weights = [float(weight) for weight in request.args.get('weights').split(',')]

        # Check if weights sum to 1
        if sum(weights) != 1:
            return {"error": "Weights must sum to 1."}, 400

        # Calculate portfolio risk
        portfolio_risk = portfolio_risk_analysis(stocks, weights)

        return {'portfolio_risk': portfolio_risk}
    except (TypeError, ValueError):
        return {"error": "Invalid input. Please ensure all fields are formatted correctly."}, 400


@portfolio_risk_calculator.route('/portfolio_risk_analysis', methods=['GET', 'POST'])
@login_required
def user_calculate_portfolio_risk():
    if request.method == 'POST':
        # Get form data
        stocks = request.form.get('stocks')
        weights = request.form.get('weights')

        # Check if any field is empty
        if not all([stocks, weights]):
            error_message = "Please fill in all fields."
            return render_template('portfolio_risk_analysis.html', error_message=error_message)

        # Convert form data to lists
        try:
            stocks = stocks.split(',')
            weights = [float(weight) for weight in weights.split(',')]
        except ValueError:
            error_message = "Invalid input. Please ensure all fields are formatted correctly."
            return render_template('portfolio_risk_analysis.html', error_message=error_message)

        # Check if weights sum to 1
        if sum(weights) != 1:
            error_message = "Weights must sum to 1."
            return render_template('portfolio_risk_analysis.html', error_message=error_message)

        # Calculate portfolio risk
        portfolio_risk = portfolio_risk_analysis(stocks, weights)

        # Save the calculation to DynamoDB
        calculation_id = str(uuid.uuid4())
        table.put_item(
            Item={
                'user_id': session['user']['id'],
                'calculation_id': calculation_id,
                'calculation_type': 'portfolio_risk',
                'input_params': str((stocks, weights)),
                'result': Decimal(str(portfolio_risk)),
                'created_at': str(datetime.utcnow())
            }
        )

        return render_template('portfolio_risk_analysis.html', portfolio_risk=portfolio_risk)

    return render_template('portfolio_risk_analysis.html')

