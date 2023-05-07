#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import yfinance as yf
import plotly.graph_objs as go

def plot_vol_smile(ticker):
    # Fetch options data for the given ticker
    opt = yf.Ticker(ticker).option_chain("2023-05-12")
    call = opt.calls
    put = opt.puts
    
    # Compute implied volatilities for each strike price
    call_iv = call["impliedVolatility"].tolist()
    put_iv = put["impliedVolatility"].tolist()
    strikes = call["strike"].tolist() + put["strike"].tolist()
    ivs = call_iv + put_iv
    
    # Sort the data by strike price
    data = sorted(list(zip(strikes, ivs)), key=lambda x: x[0])
    strikes = [d[0] for d in data]
    ivs = [d[1] for d in data]
    
    # Create 2D grid of strike prices and time to expiration
    max_strike = max(strikes)
    min_strike = min(strikes)
    ttm = [30, 60, 90, 120, 150, 180]
    strike_step = (max_strike - min_strike) / 100
    strikes = [min_strike + i * strike_step for i in range(101)]
    X, Y = [], []
    for t in ttm:
        X.append(strikes)
        Y.append([t] * 101)
    
    # Create 3D surface plot of implied volatilities
    data = go.Surface(x=X, y=Y, z=[ivs]*len(ttm), colorscale="Viridis", showscale=False)
    layout = go.Layout(title=f"Implied Volatility Smile for {ticker}", scene=dict(xaxis_title="Strike", yaxis_title="Time to Expiration", zaxis_title="Implied Volatility"))
    fig = go.Figure(data=[data], layout=layout)
    fig.show()

# Example usage
plot_vol_smile("AMZN")


# # For host in a web server using flask 

# In[ ]:


from flask import Flask, render_template, request
import yfinance as yf
import pandas as pd
import plotly.express as px


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ticker = request.form['ticker']
        option_type = request.form['option_type']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        min_strike = request.form['min_strike']
        return plot(ticker, option_type, start_date, end_date, min_strike)
    else:
        return render_template('index.html')

def plot(ticker, option_type, start_date, end_date, min_strike):
    df = yf.download(ticker, start=start_date, end=end_date, group_by='Ticker')
    options = df.options
    chain = df.option_chain(options[0])
    calls = chain.calls
    puts = chain.puts

    if option_type == 'call':
        data = calls
    elif option_type == 'put':
        data = puts
    else:
        return 'Invalid option type'

    data = data[data['inTheMoney'] == False]
    data = data[data['strike'] >= float(min_strike)]

    strikes = data['strike'].unique()
    expirations = data['expiration'].unique()

    ivs = []
    for s in strikes:
        iv_row = []
        for e in expirations:
            option = data[(data['expiration'] == e) & (data['strike'] == s)]
            if not option.empty:
                iv_row.append(option['impliedVolatility'].iloc[0])
            else:
                iv_row.append(None)
        ivs.append(iv_row)

    fig = px.surface(x=expirations, y=strikes, z=ivs)
    fig.update_layout(title=f'Volatility Smile for {ticker.upper()} {option_type.capitalize()} Options',
                      scene=dict(xaxis_title='Expiration', yaxis_title='Strike', zaxis_title='Implied Volatility'))

    return render_template('plot.html', plot=fig.to_html(full_html=False))


if __name__ == '__main__':
    app.run(debug=True)

