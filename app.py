from flask import Flask, render_template, request
from gunsan_strength.core import get_gunsan_strength
from gunsan_strength.plots import plot_gunsan_strength
import yfinance as yf
import pandas as pd
from datetime import date
import plotly.io as pio
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    plot_html = None

    if request.method == 'POST':
        ticker = request.form.get('ticker')
        freq = request.form.get('frequency')
        signal_window = int(request.form.get('signal_window', 14))

        # Dates
        start_date = '1995-01-01'
        end_date = date.today().strftime('%Y-%m-%d')

        try:
            df = yf.download(ticker, start=start_date, end=end_date, interval=freq, multi_level_index=False)
            df.reset_index(inplace=True)

            if df.empty:
                return render_template('index.html', error="No data found. Try another ticker or timeframe.")

            gsi = get_gunsan_strength(df, signal_window)
            fig = plot_gunsan_strength(gsi)

            plot_html = pio.to_html(fig, full_html=False)

        except Exception as e:
            return render_template('index.html', error=str(e))

    return render_template('index.html', plot_html=plot_html)
