import os
from ast import literal_eval

import boto3
from boto3.dynamodb.conditions import Key
from flask import Flask, render_template, session

from blueprints.auth import auth, login_required
from blueprints.black_scholes_calculator import black_scholes_calculator, black_scholes_limiter
from blueprints.portfolio_risk_analysis import portfolio_risk_calculator, portfolio_risk_limiter
from data_formatting import get_readable_name, format_input_parameters, format_timestamp

dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
table = dynamodb.Table('UserCalculations')


def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.secret_key = os.environ.get('SECRET_KEY')

    # Register blueprints
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(black_scholes_calculator)
    app.register_blueprint(portfolio_risk_calculator)

    black_scholes_limiter.init_app(app)
    portfolio_risk_limiter.init_app(app)

    @app.route('/')
    def home():
        return render_template('home.html', show_modal=False)

    @app.route('/previous_calculations')
    @login_required
    def previous_calculations():
        response = table.query(
            KeyConditionExpression=Key('user_id').eq(session['user']['id'])
        )
        calculations = response['Items']

        # Formatting the data
        for calculation in calculations:
            # Make the calculation type readable
            calculation_type = calculation.get('calculation_type')
            if calculation_type:
                calculation['calculation_type'] = get_readable_name(calculation_type)
            else:
                calculation['calculation_type'] = "Unknown Calculation Type"

            # Format input parameters based on the calculation type
            inputs = calculation.get('input_params')
            if inputs:
                calculation['input_params'] = format_input_parameters(calculation_type, literal_eval(inputs))
            else:
                calculation['input_params'] = "N/A"

            # Format the timestamp
            timestamp = calculation.get('created_at')
            if timestamp:
                calculation['created_at'] = format_timestamp(timestamp)
            else:
                calculation['created_at'] = "N/A"

        return render_template('previous_calculations.html', previous_calculations=calculations, show_modal=False)

    return app


app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
