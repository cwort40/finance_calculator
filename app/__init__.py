from flask import Flask, render_template
from blueprints.auth import auth
from blueprints.black_scholes_calculator import black_scholes_calculator
from blueprints.portfolio_risk_analysis import portfolio_risk_calculator
import os


def create_app():
    app = Flask(__name__, template_folder='../templates')
    app.secret_key = os.environ.get('SECRET_KEY')  # Make sure to set a SECRET_KEY

    # Register blueprints
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(black_scholes_calculator)
    app.register_blueprint(portfolio_risk_calculator)

    @app.route('/')
    def home():
        return render_template('home.html')  # Render the home page template

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
