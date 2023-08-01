from flask import Blueprint, request, render_template

from utils import black_scholes_call_option

black_scholes_calculator = Blueprint('black_scholes_calculator', __name__, template_folder='../templates')


@black_scholes_calculator.route('/calculate_option_price', methods=['GET', 'POST'])
def calculate_option_price():
    if request.method == 'GET':
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

    elif request.method == 'POST':
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

        return render_template('black_scholes_calculator.html', option_price=option_price)

    return render_template('black_scholes_calculator.html')