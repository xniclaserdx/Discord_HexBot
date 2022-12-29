import yfinance as yahooFinance
import datetime
import interactions
from interactions.ext.files import command_send
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io


def get_market_price(ticker):
    try:
        try:
            financeData = yahooFinance.Ticker(ticker)
            return f" Market Price of {financeData.info['shortName']} - {financeData.info['regularMarketPrice']} $"
        except:
            return f" Market Price: {financeData.info['regularMarketPrice']} $"
    except:
        return f'{ticker.upper()} could not be resolved.'
def get_history(ticker):
    now = datetime.datetime.now()
    start_date = (now - datetime.timedelta(days=365*2)).strftime("%Y-%m-%d")
    end_date = (now + datetime.timedelta(days=365*2)).strftime("%Y-%m-%d")
    data = yahooFinance.download(ticker, start_date, end_date)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(data.index, data['Close'], color='#43B581')

    ax.spines['top'].set_color('white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('white')

    ax.tick_params(axis='both', colors='white')

    ax.set_xlabel('Date', color='white')
    ax.set_ylabel('Close Price (USD)', color='white')
    ax.set_title(f'{ticker.upper()} Stock Price', color='white')
    imageByteArr = io.BytesIO()
    plt.savefig(imageByteArr, dpi=200, transparent=True)
    imageByteArr.seek(0)
    return imageByteArr

class FinanceModule(interactions.Extension):
    def __init__(self,client):
        self.client = client

    @interactions.extension_command(
        name ="hex_stock_price",
        description = "Checks the current value of a stock",
        options = [
            interactions.Option(
                name = "ticker",
                description = "Stock ticker",
                type = interactions.OptionType.STRING,
                required = True
            )
        ]
    )
    async def finance_stock_command(self,ctx: interactions.CommandContext, ticker: str):
        await ctx.send(get_market_price(ticker))

    @interactions.extension_command( 
        name ="hex_stock_plot",
        description = "Plot a graph showing the stock closing prices of the last two years.",
        options = [
            interactions.Option(
                name = "ticker",
                description = "Stock ticker",
                type = interactions.OptionType.STRING,
                required = True
            )
        ]
    )
    async def finance_plot_command(self,ctx: interactions.CommandContext, ticker: str):
        await command_send(ctx,"",files = interactions.File(fp = get_history(ticker),filename='plot.png'))
        
def setup(client):
    FinanceModule(client)
