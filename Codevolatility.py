#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, render_template, request, redirect, url_for
import yfinance as yf

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pricer')
def pricer():
    return render_template('pricer.html')

@app.route('/curves_rates')
def curves_rates():
    return render_template('curves_rates.html')

@app.route('/', methods=['POST'])
def plot():
    ticker = request.form['ticker']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    option_type = request.form['option_type']
    exp_date = request.form['exp_date']

    stock = yf.Ticker(ticker)
    df = stock.option_chain(exp_date)[option_type]
    df = df[(df['contractSymbol'].str[-1:] == 'C') | (df['contractSymbol'].str[-1:] == 'P')]

    # Plotting code here
    plot_div = "Plot will be displayed here"

    return render_template('index.html', plot_div=plot_div)

if __name__ == '__main__':
    app.run(debug=True)
