from flask import Flask, request, render_template
from .utils import black_scholes_call_option, portfolio_risk_analysis

app = Flask(__name__, template_folder='../templates')


@app.route('/calculate_option_price', methods=['GET', 'POST'])
def calculate_option_price():
    if request.method == 'POST':
        data = request.get_json() or request.form
        S, K, T, r, sigma = data.get('S'), data.get('K'), data.get('T'), data.get('r'), data.get('sigma')

        if not all([S, K, T, r, sigma]):
            error_message = "Please fill in all fields."
            return render_template('calculator.html', error_message=error_message)

        try:
            S, K, T, r, sigma = float(S), float(K), float(T), float(r), float(sigma)
        except ValueError:
            error_message = "Invalid input. Please ensure all fields are numbers."
            return render_template('calculator.html', error_message=error_message)

        option_price = black_scholes_call_option(S, K, T, r, sigma)
        return render_template('calculator.html', option_price=option_price)

    return render_template('calculator.html')


@app.route('/portfolio_risk_analysis', methods=['GET', 'POST'])
def calculate_portfolio_risk():
    if request.method == 'POST':
        data = request.get_json() or request.form
        stocks, weights = data.get('stocks'), data.get('weights')

        if not all([stocks, weights]):
            error_message = "Please fill in all fields."
            return render_template('portfolio_risk_analysis.html', error_message=error_message)

        try:
            stocks = stocks.split(',')
            weights = [float(weight) for weight in weights.split(',')]
        except ValueError:
            error_message = "Invalid input. Please ensure all fields are formatted correctly."
            return render_template('portfolio_risk_analysis.html', error_message=error_message)

        if sum(weights) != 1:
            error_message = "Weights must sum to 1."
            return render_template('portfolio_risk_analysis.html', error_message=error_message)

        portfolio_risk = portfolio_risk_analysis(stocks, weights)
        return render_template('portfolio_risk_analysis.html', portfolio_risk=portfolio_risk)

    return render_template('portfolio_risk_analysis.html')


if __name__ == '__main__':
    app.run(debug=True)


