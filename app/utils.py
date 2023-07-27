import numpy as np
import scipy.stats as si


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

    return call

