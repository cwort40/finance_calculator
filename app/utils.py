import numpy as np
import pandas as pd
from pandas_datareader import data as web
import scipy.stats as si
from datetime import datetime, timedelta


def black_scholes_call_option(S, K, T, r, sigma):
    """
    Calculate Call Option Price using Black-Scholes model
    S : Stock Price
    K : Strike Price
    T : Time to Maturity
    r : Risk-Free Rate
    sigma : Volatility of underlying asset
    """
    # Calculate d1 and d2 parameters
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = (np.log(S / K) + (r - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))

    # Calculate Call Option Price
    call = (S * si.norm.cdf(d1, 0.0, 1.0) - K * np.exp(-r * T) * si.norm.cdf(d2, 0.0, 1.0))

    return round(call, 3)

# TODO: improve this calculator and add logic for it in __init__.py and finish the template
def portfolio_risk_analysis(stocks, weights):
    """
    Calculate the portfolio risk.

    Args:
    stocks : list of strings
        List of stock ticker symbols.
    weights : list of floats
        The corresponding weights of each stock in the portfolio.

    Returns:
    float
        The portfolio risk.
    """

    # Fetch the historical data
    start_date = datetime.now() - timedelta(days=365)  # 1 year of historical data
    end_date = datetime.now()
    data = pd.DataFrame()

    for stock in stocks:
        data[stock] = web.DataReader(stock, 'yahoo', start_date, end_date)['Adj Close']

    # Calculate the log of returns
    log_returns = np.log(data / data.shift(1))

    # Calculate the covariance matrix on the log returns
    cov_matrix = log_returns.cov()

    # Calculate the portfolio variance
    portfolio_variance = np.dot(weights.T, np.dot(cov_matrix, weights))

    # Calculate the portfolio volatility aka standard deviation
    portfolio_volatility = np.sqrt(portfolio_variance)

    return portfolio_volatility
