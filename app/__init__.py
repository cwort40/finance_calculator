from flask import Flask, request, render_template

from blueprints import black_scholes_calculator
from .utils import portfolio_risk_analysis

app = Flask(__name__, template_folder='../templates')

app.register_blueprint(black_scholes_calculator.black_scholes_calculator)


# TODO: figure out why there is a 404 error when running pytest and then configure blueprint to accommodate both http
#  requests and template requests. then implement a blueprint for the portfolio risk function

@app.route('/portfolio_risk_analysis', methods=['GET', 'POST'])
def calculate_portfolio_risk():
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

        return render_template('portfolio_risk_analysis.html', portfolio_risk=portfolio_risk)

    return render_template('portfolio_risk_analysis.html')


if __name__ == '__main__':
    app.run(debug=True)
