import os

import boto3
from boto3.dynamodb.conditions import Key
from flask import Flask, render_template, session

from blueprints.auth import auth, login_required
from blueprints.black_scholes_calculator import black_scholes_calculator
from blueprints.portfolio_risk_analysis import portfolio_risk_calculator

dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
table = dynamodb.Table('UserCalculations')


def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.secret_key = os.environ.get('SECRET_KEY')

    # Register blueprints
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(black_scholes_calculator)
    app.register_blueprint(portfolio_risk_calculator)

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
        return render_template('previous_calculations.html', previous_calculations=calculations, show_modal=False)

    return app


app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
