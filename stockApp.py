# Import required libraries
import streamlit as st
import pandas as pd
from PIL import Image
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr

# a workaround for how yahoo handles and displays stock data
yf.pdr_override()


# Add title and Image
st.write("""
# Stock Market Web Application
**Visually** show data on a stock!
""")

image = Image.open('F:/College/Programming/Python/Git/price_tracker/stock.jpg')
st.image(image, use_column_width = True)

st.sidebar.header("User Input")


# Obtains user inputs (start date, end date and company stock ticker) from the sidebar
def get_input():
    start_date = st.sidebar.text_input("Start Date", "2021-06-01")
    end_date = st.sidebar.text_input("End Date", "2021-06-19")
    stock_symbol = st.sidebar.text_input("Stock Symbol", "TSLA")

    return start_date, end_date, stock_symbol


# Returns Name of company based on stock ticker/symbol
def get_company_name(symbol):
    ticker = yf.Ticker(symbol)

    return ticker.info['longName']


# Returns stock data 
def get_data(symbol, start_date, end_date):
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)

    data = pdr.get_data_yahoo(symbol, start, end)
    # print(data.columns)

    start_row = 0
    end_row = 0

    for i in range(len(data)):
        if start <= pd.to_datetime(data.index[i]):
            start_row = i
            break

    for j in range(len(data)):
        # starts from the last row and moves upwards
        if end >= pd.to_datetime(data.index[len(data)-1-j]):
            end_row = len(data) - 1 - j
            break

    data = data.set_index(pd.to_datetime(data.index.values))

    return data.iloc[start_row:end_row+1, :]


start, end, symbol = get_input()

data = get_data(symbol, start, end)
# print(data)

company_name = get_company_name(symbol.upper())

# Get Closing price
st.header(company_name+"\t\tClose Price:\n")
st.line_chart(data['Close'])

# Display Volume
st.header(company_name+"\t\tVolume:\n")
st.line_chart(data['Volume'])

# Display statistics
st.header("Data Statistics")
st.write(data.describe())
