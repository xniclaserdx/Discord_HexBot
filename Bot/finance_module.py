"""Finance module for stock market data retrieval and visualization."""
import yfinance as yahooFinance
import datetime
import interactions
from interactions.ext.files import command_send
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io
import numpy as np


def get_market_price(ticker: str) -> str:
    """
    Get the current market price for a given stock ticker.
    
    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'GOOGL')
        
    Returns:
        String with the current market price or error message
    """
    try:
        finance_data = yahooFinance.Ticker(ticker)
        try:
            short_name = finance_data.info.get('shortName', ticker.upper())
            market_price = finance_data.info['regularMarketPrice']
            return f"Market Price of {short_name} - {market_price} $"
        except KeyError:
            market_price = finance_data.info.get('regularMarketPrice')
            if market_price:
                return f"Market Price: {market_price} $"
            return f"{ticker.upper()} - Price data not available."
    except Exception as e:
        return f"{ticker.upper()} could not be resolved."


def get_history(ticker: str) -> io.BytesIO:
    """
    Generate a 2-year price history chart for a stock.
    
    Args:
        ticker: Stock ticker symbol
        
    Returns:
        BytesIO object containing the PNG chart
    """
    now = datetime.datetime.now()
    start_date = (now - datetime.timedelta(days=365*2)).strftime("%Y-%m-%d")
    end_date = (now + datetime.timedelta(days=365*2)).strftime("%Y-%m-%d")
    
    data = yahooFinance.download(ticker, start_date, end_date)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    try:
        ax.plot(data.index, data['Close'], color='#43B581')

        ax.spines['top'].set_color('white')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['right'].set_color('white')

        ax.tick_params(axis='both', colors='white')

        ax.set_xlabel('Date', color='white')
        ax.set_ylabel('Close Price (USD)', color='white')
        ax.set_title(f'{ticker.upper()} Stock Price', color='white')
        
        image_byte_arr = io.BytesIO()
        plt.savefig(image_byte_arr, dpi=200, transparent=True)
        image_byte_arr.seek(0)
        return image_byte_arr
    finally:
        # Clean up matplotlib resources
        plt.close(fig)


def get_stock_prediction(ticker: str) -> str:
    """
    Predict stock trend using moving averages and momentum analysis.
    
    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'GOOGL')
        
    Returns:
        String with prediction analysis or error message
    """
    try:
        # Get historical data for the last 60 days
        now = datetime.datetime.now()
        start_date = (now - datetime.timedelta(days=60)).strftime("%Y-%m-%d")
        end_date = now.strftime("%Y-%m-%d")
        
        data = yahooFinance.download(ticker, start_date, end_date, progress=False)
        
        if data.empty or len(data) < 20:
            return f"{ticker.upper()} - Insufficient data for prediction."
        
        # Get stock info
        finance_data = yahooFinance.Ticker(ticker)
        short_name = finance_data.info.get('shortName', ticker.upper())
        
        # Calculate moving averages
        close_prices = data['Close'].values
        ma_7 = np.mean(close_prices[-7:])  # 7-day moving average
        ma_20 = np.mean(close_prices[-20:])  # 20-day moving average
        current_price = close_prices[-1]
        
        # Calculate momentum (price change over last 7 days)
        momentum = ((current_price - close_prices[-7]) / close_prices[-7]) * 100
        
        # Calculate volatility (standard deviation)
        volatility = np.std(close_prices[-20:])
        
        # Determine trend
        if ma_7 > ma_20:
            trend = "BULLISH 📈"
            if momentum > 2:
                strength = "Strong"
            elif momentum > 0:
                strength = "Moderate"
            else:
                strength = "Weak"
        elif ma_7 < ma_20:
            trend = "BEARISH 📉"
            if momentum < -2:
                strength = "Strong"
            elif momentum < 0:
                strength = "Moderate"
            else:
                strength = "Weak"
        else:
            trend = "NEUTRAL ➡️"
            strength = "Consolidating"
        
        # Build prediction message
        prediction = f"**Stock Prediction for {short_name}**\n\n"
        prediction += f"Current Price: ${current_price:.2f}\n"
        prediction += f"7-Day MA: ${ma_7:.2f}\n"
        prediction += f"20-Day MA: ${ma_20:.2f}\n"
        prediction += f"7-Day Momentum: {momentum:+.2f}%\n\n"
        prediction += f"**Trend: {trend}** ({strength})\n"
        prediction += f"Volatility: ${volatility:.2f}\n\n"
        
        # Add recommendation
        if trend == "BULLISH 📈" and momentum > 1:
            prediction += "💡 Prediction: Short-term upward trend likely to continue."
        elif trend == "BEARISH 📉" and momentum < -1:
            prediction += "💡 Prediction: Short-term downward trend likely to continue."
        elif abs(momentum) < 1:
            prediction += "💡 Prediction: Price consolidation expected in the short term."
        else:
            prediction += "💡 Prediction: Trend reversal may be forming."
        
        prediction += "\n\n⚠️ *This is not financial advice. Past performance does not guarantee future results.*"
        
        return prediction
        
    except Exception as e:
        return f"{ticker.upper()} - Unable to generate prediction. Error: {str(e)}"


class FinanceModule(interactions.Extension):
    """Extension module for finance and stock market commands."""
    
    def __init__(self, client):
        self.client = client

    @interactions.extension_command(
        name="hex_stock_price",
        description="Checks the current value of a stock",
        options=[
            interactions.Option(
                name="ticker",
                description="Stock ticker",
                type=interactions.OptionType.STRING,
                required=True
            )
        ]
    )
    async def finance_stock_command(self, ctx: interactions.CommandContext, ticker: str):
        """Get current stock price for the given ticker."""
        await ctx.send(get_market_price(ticker))

    @interactions.extension_command( 
        name="hex_stock_plot",
        description="Plot a graph showing the stock closing prices of the last two years.",
        options=[
            interactions.Option(
                name="ticker",
                description="Stock ticker",
                type=interactions.OptionType.STRING,
                required=True
            )
        ]
    )
    async def finance_plot_command(self, ctx: interactions.CommandContext, ticker: str):
        """Generate and send a 2-year stock price chart."""
        await command_send(ctx, "", files=interactions.File(fp=get_history(ticker), filename='plot.png'))

    @interactions.extension_command(
        name="hex_stock_predict",
        description="Predict stock trend using technical analysis (moving averages and momentum).",
        options=[
            interactions.Option(
                name="ticker",
                description="Stock ticker",
                type=interactions.OptionType.STRING,
                required=True
            )
        ]
    )
    async def finance_predict_command(self, ctx: interactions.CommandContext, ticker: str):
        """Generate stock prediction based on technical analysis."""
        await ctx.send(get_stock_prediction(ticker))
        

def setup(client):
    """Set up the FinanceModule extension."""
    FinanceModule(client)
