#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
from scipy.stats import norm

def black_scholes(S, K, T, r, sigma):
    """
    Calculate the price and Greeks of a European call option using the Black-Scholes model.
    
    Args:
        S (float): The current price of the underlying asset.
        K (float): The strike price of the option.
        T (float): The time to expiration of the option in years.
        r (float): The risk-free interest rate.
        sigma (float): The volatility of the underlying asset.
    
    Returns:
        tuple: A tuple containing the price of the option and its Greeks (delta, gamma, vega, theta, rho).
    """
    d1 = (np.log(S/K) + (r + sigma**2/2)*T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    # Calculate the price of the option
    price = S * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2)
    
    # Calculate the Greeks
    delta = norm.cdf(d1)
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    vega = S * norm.pdf(d1) * np.sqrt(T)
    theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) -
             r * K * np.exp(-r*T) * norm.cdf(d2))
    rho = K * T * np.exp(-r*T) * norm.cdf(d2)
    
    return price, delta, gamma, vega, theta, rho


# In[2]:


# Set the input parameters
S = 100  # current price of the underlying asset
K = 105  # strike price of the option
T = 0.5  # time to expiration of the option in years
r = 0.05  # risk-free interest rate
sigma = 0.2  # volatility of the underlying asset

# Calculate the price and Greeks of the option
price, delta, gamma, vega, theta, rho = black_scholes(S, K, T, r, sigma)

# Print the results
print('Price of the option: ${:.2f}'.format(price))
print('Delta: {:.2f}'.format(delta))
print('Gamma: {:.2f}'.format(gamma))
print('Vega: {:.2f}'.format(vega))
print('Theta: {:.2f}'.format(theta))
print('Rho: {:.2f}'.format(rho))


# In[ ]:




