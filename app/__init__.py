from flask import Flask, request, render_template
from .utils import black_scholes_call_option, portfolio_risk_analysis

app = Flask(__name__, template_folder='../templates')


@app.route('/calculate_option_price', methods=['GET', 'POST'])
def calculate_option_price():
    if request.method == 'POST':
        # Get form data
        S = request.form.get('S')
        K = request.form.get('K')
        T = request.form.get('T')
        r = request.form.get('r')
        sigma = request.form.get('sigma')

        # Check if any field is empty
        if not all([S, K, T, r, sigma]):
            error_message = "Please fill in all fields."
            return render_template('calculator.html', error_message=error_message)

        # Convert form data to floats
        try:
            S = float(S)
            K = float(K)
            T = float(T)
            r = float(r)
            sigma = float(sigma)
        except ValueError:
            error_message = "Invalid input. Please ensure all fields are numbers."
            return render_template('calculator.html', error_message=error_message)

        # Calculate option price
        option_price = black_scholes_call_option(S, K, T, r, sigma)

        return render_template('calculator.html', option_price=option_price)

    return render_template('calculator.html')


# TODO: add portfolio risk analysis
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


