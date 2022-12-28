import yfinance as yahooFinance
import datetime
import interactions

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

class FinanceModule(interactions.Extension):
    def __init__(self,client):
        self.client = client

    # command to get stock values
    @interactions.extension_command(
        name ="hex_finance_price",
        description = "Checks the value of a stock (?); to be updated",
        options = [
            interactions.Option(
                name = "stock",
                description = "Stock name",
                type = interactions.OptionType.STRING,
                required = True
            )
        ]
    )
    async def finance_price_command(self,ctx: interactions.CommandContext, stock: str):
        await ctx.send(get_market_price(stock))

def setup(client):
    FinanceModule(client)