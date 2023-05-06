#!/usr/bin/env python
# coding: utf-8

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
        return plot(ticker, option_type, start_date, end_date)
    else:
        return render_template('index.html')

def plot(ticker, option_type, start_date, end_date):
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

