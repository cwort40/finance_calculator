from flask import Flask, request, render_template
from .utils import black_scholes_call_option

app = Flask(__name__, template_folder='../templates')


@app.route('/calculate_option_price', methods=['GET', 'POST'])
def calculate_option_price():

    if request.method == 'POST':
        S = float(request.form.get('S'))
        K = float(request.form.get('K'))
        T = float(request.form.get('T'))
        r = float(request.form.get('r'))
        sigma = float(request.form.get('sigma'))

        option_price = black_scholes_call_option(S, K, T, r, sigma)

        return render_template('calculator.html', option_price=option_price)

    return render_template('calculator.html')


if __name__ == '__main__':
    app.run(debug=True)
