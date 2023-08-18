import uuid
from datetime import datetime

import boto3
from flask import Blueprint, request, render_template, session

from blueprints.auth import login_required
from utils import black_scholes_call_option

from decimal import Decimal

from flask_limiter.util import get_remote_address
from flask_limiter import Limiter


black_scholes_limiter = Limiter(key_func=get_remote_address)

black_scholes_calculator = Blueprint('black_scholes_calculator', __name__, template_folder='../templates')

dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
table = dynamodb.Table('UserCalculations')


# Adding login_required decorator for now, will implement API auth tokens later
@black_scholes_calculator.route('/api/calculate_option_price', methods=['GET'])
@black_scholes_limiter.limit("10 per minute")
def api_calculate_option_price():
    try:
        S = float(request.args.get('S'))
        K = float(request.args.get('K'))
        T = float(request.args.get('T'))
        r = float(request.args.get('r'))
        sigma = float(request.args.get('sigma'))

        option_price = black_scholes_call_option(S, K, T, r, sigma)

        return {'option_price': option_price}
    except (TypeError, ValueError):
        return {"error": "Invalid input. Please ensure all fields are numbers."}, 400


@black_scholes_calculator.route('/calculate_option_price', methods=['GET', 'POST'])
@login_required
def user_calculate_option_price():
    if request.method == 'POST':
        S = request.form.get('S')
        K = request.form.get('K')
        T = request.form.get('T')
        r = request.form.get('r')
        sigma = request.form.get('sigma')

        # Check if any field is empty
        if not all([S, K, T, r, sigma]):
            error_message = "Please fill in all fields."
            return render_template('black_scholes_calculator.html', error_message=error_message)

        # Convert form data to floats
        try:
            S = float(S)
            K = float(K)
            T = float(T)
            r = float(r)
            sigma = float(sigma)
        except ValueError:
            error_message = "Invalid input. Please ensure all fields are numbers."
            return render_template('black_scholes_calculator.html', error_message=error_message)

        # Calculate option price
        option_price = black_scholes_call_option(S, K, T, r, sigma)

        # Save the calculation to DynamoDB
        calculation_id = str(uuid.uuid4())
        table.put_item(
            Item={
                'user_id': session['user']['id'],
                'calculation_id': calculation_id,
                'calculation_type': 'option_price',
                'input_params': str((S, K, T, r, sigma)),
                'result': Decimal(str(option_price)),
                'created_at': str(datetime.utcnow())
            }
        )

        return render_template('black_scholes_calculator.html', option_price=option_price)

    return render_template('black_scholes_calculator.html')
