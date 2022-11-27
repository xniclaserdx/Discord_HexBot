import yfinance as yahooFinance
import datetime


def get_market_price(ticker):
    try:
        try:
            financeData = yahooFinance.Ticker(ticker)
            return f" Market Price of {financeData.info['shortName']} - {financeData.info['regularMarketPrice']} $"
        except:
            return f" Market Price: {financeData.info['regularMarketPrice']} $"
    except:
        return f"No data found."
def get_history(ticker):
    start_date = "2020-01-01"
    end_date = "2022-01-01"

    # Get the data
    data = yahooFinance.download(ticker, start_date, end_date)

    print(data.tail())

