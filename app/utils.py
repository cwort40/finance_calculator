from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import scipy.stats as si
import yfinance as yf


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


def portfolio_risk_analysis(stocks: list, weights: list) -> float:
    """
    Analyze Portfolio Risk based on stock prices and weights
    stocks : List of stock symbols
    weights : List of weights corresponding to stocks

    Returns the portfolio volatility
    """
    weights = np.array(weights)
    stocks = [s.strip() for s in stocks]

    # Normalize weights if they don't sum to 1
    weights = weights / np.sum(weights)

    try:
        start_date = datetime.now() - timedelta(days=365)
        end_date = datetime.now()
        data = yf.download(stocks, start=start_date, end=end_date)["Adj Close"]
    except ConnectionError:
        print("Failed to download stock data.")
        return 0

    log_returns = pd.DataFrame(np.log(data / data.shift(1)))
    cov_matrix = log_returns.cov()
    portfolio_variance = np.dot(weights.T, np.dot(cov_matrix, weights))
    portfolio_volatility = round(np.sqrt(portfolio_variance), 3)

    return portfolio_volatility
