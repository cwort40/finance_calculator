from datetime import datetime


def get_readable_name(calculation_name):
    readable_names = {
        'portfolio_risk': 'Portfolio Risk',
        'option_price': 'Option Price'
    }
    return readable_names.get(calculation_name, calculation_name)


def format_input_parameters(calculation_name, parameters):
    if calculation_name == 'portfolio_risk':
        stocks, weights = parameters
        formatted_params = f"Stocks: {', '.join(stocks)}, Weights: {', '.join(map(str, weights))}"
    elif calculation_name == 'option_price':
        S, K, T, r, sigma = parameters
        formatted_params = f"S: {S}, K: {K}, T: {T}, r: {r}, sigma: {sigma}"
    else:
        formatted_params = str(parameters)
    return formatted_params


def format_timestamp(timestamp):
    date_object = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
    return date_object.strftime('%Y-%m-%d %H:%M:%S')
