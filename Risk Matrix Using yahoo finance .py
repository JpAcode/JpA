#!/usr/bin/env python
# coding: utf-8

# In[2]:


import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

# Download stock data
tickers = ['AAPL', 'GOOGL', 'TSLA', 'MSFT']
data = yf.download(tickers, start='2020-01-01', end='2021-01-01')['Adj Close']
returns = data.pct_change().dropna()

# Calculate average returns and covariance matrix
mean_returns = returns.mean()
cov_matrix = returns.cov()

# Define risk levels and their corresponding colors
risk_levels = {
    'Low': '#008000',     # green
    'Medium': '#FFFF00',  # yellow
    'High': '#FFA500',    # orange
    'Critical': '#FF0000' # red
}

# Define the x-axis and y-axis labels
x_axis_labels = ['Likelihood', 'Low', 'Medium', 'High', 'Critical']
y_axis_labels = ['Impact', 'Low', 'Medium', 'High', 'Critical']

# Calculate the risk levels for each stock
risk_levels_matrix = np.zeros((len(y_axis_labels)-1, len(x_axis_labels)-1))
for i in range(len(y_axis_labels)-1):
    for j in range(len(x_axis_labels)-1):
        # Calculate the index of the current risk level
        impact_index = i+1
        likelihood_index = j+1
        risk_level = None
        if mean_returns[tickers[impact_index-1]] > 0 and cov_matrix.iloc[impact_index-1, impact_index-1] > 0:
            risk = mean_returns[tickers[impact_index-1]] / cov_matrix.iloc[impact_index-1, impact_index-1]
            if risk < 0.1:
                risk_level = 'Low'
            elif risk < 0.5:
                risk_level = 'Medium'
            elif risk < 0.8:
                risk_level = 'High'
            else:
                risk_level = 'Critical'
        risk_levels_matrix[i, j] = list(risk_levels.keys()).index(risk_level)

# Create the risk matrix
fig, ax = plt.subplots()
for i, y_label in enumerate(y_axis_labels[:-1]):
    for j, x_label in enumerate(x_axis_labels[:-1]):
        # Get the risk level index
        risk_level_index = int(risk_levels_matrix[i, j])
        
        # Set the color of the current risk level
        color = risk_levels[list(risk_levels.keys())[risk_level_index]]
        
        # Draw a rectangle for the current risk level
        ax.add_patch(plt.Rectangle((j, i), 1, 1, fill=True, color=color, alpha=0.5))
        
        # Add the stock ticker to the rectangle
        ax.text(j + 0.5, i + 0.5, tickers[i], ha='center', va='center', fontsize=10)

# Add axis labels and title
ax.set_xticks(range(len(x_axis_labels)))
ax.set_xticklabels(x_axis_labels)
ax.set_yticks(range(len(y_axis_labels)))
ax.set_yticklabels(y_axis_labels)
ax.set_xlabel('Likelihood')
ax.set_ylabel('Impact')


# In[ ]:




