from flask import Flask

from blueprints.black_scholes_calculator import black_scholes_calculator
from blueprints.portfolio_risk_analysis import portfolio_risk_calculator

app = Flask(__name__, template_folder='../templates')

app.register_blueprint(black_scholes_calculator)

app.register_blueprint(portfolio_risk_calculator)

if __name__ == '__main__':
    app.run(debug=True)
