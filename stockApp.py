# Import required libraries
import streamlit as st
import pandas as pd
import yfinance as yf
import datetime as dt
import requests
from PIL import Image
from twilio.rest import Client
from dotenv import dotenv_values
from pandas_datareader import data as pdr

# a workaround for how yahoo handles and displays stock data
yf.pdr_override()

CONFIG = dotenv_values(".env")
STOCK_PARAMETERS = {
        "function": "TIME_SERIES_DAILY",
        "symbol": str,
        "apikey": CONFIG.get("STOCK_API_KEY")
        }
NEWS_PARAMETERS = {
        "apiKey": CONFIG.get("NEWS_API_KEY"),
        "qInTitle": str
        }


class StockApp:
    def __init__(self):

        self.headlines = []
        self.briefs = []
        self.start = None
        self.end = None
        self.symbol = None
        self.data = None
        self.company_name = None

        # Add title and Image
        st.write("""
        # Stock Market Web Application
        **Visually** show data on a stock!
        """)

        image = Image.open(CONFIG.get("STOCK_IMG_FILE"))
        st.image(image, use_column_width=True)

        st.sidebar.header("User Input")

        self.get_user_input()

        self.get_yahoo_data()
        self.get_company_name()

    # Obtains user inputs (start date, end date and company stock ticker) from the sidebar
    def get_user_input(self):
        self.start = st.sidebar.text_input("Start Date", "2021-06-01")
        self.end = st.sidebar.text_input("End Date", "2021-06-19")
        self.symbol = st.sidebar.text_input("Stock Symbol", "TSLA")

    # Returns Name of company based on stock ticker/symbol
    def get_company_name(self):
        ticker = yf.Ticker(self.symbol.upper())

        self.company_name = ticker.info['longName']

    # Returns stock data
    def get_yahoo_data(self):
        start = pd.to_datetime(self.start)
        end = pd.to_datetime(self.end)

        data = pdr.get_data_yahoo(self.symbol, start, end)
        # print(data.columns)

        start_row = 0
        end_row = 0

        for i in range(len(data)):
            if start <= pd.to_datetime(data.index[i]):
                start_row = i
                break

        for j in range(len(data)):
            # starts from the last row and moves upwards
            if end >= pd.to_datetime(data.index[len(data) - 1 - j]):
                end_row = len(data) - 1 - j
                break

        data = data.set_index(pd.to_datetime(data.index.values))

        self.data = data.iloc[start_row:end_row + 1, :]


# print(data)
stock = StockApp()

# Get Closing price
st.header(stock.company_name + "\t\tClose Price:\n")
st.line_chart(stock.data['Close'])

# Display Volume
st.header(stock.company_name + "\t\tVolume:\n")
st.line_chart(stock.data['Volume'])

# Display statistics
st.header("Data Statistics")
st.write(stock.data.describe())
