# Discord HexBot 🤖

A versatile Discord bot written in Python with multiple utility features including mathematical calculations, stock market data, Minecraft server status checking, and more.

## 📋 Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Commands Reference](#commands-reference)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Authors](#authors)

## ✨ Features

- **Core Commands**: Date display, greetings, random number generation, and coin flipping
- **Mathematical Operations**: Base conversion and advanced matrix calculations with LaTeX rendering
- **Finance Module**: Real-time stock prices, historical price charts, and stock trend predictions using technical analysis
- **Minecraft Integration**: Server status and player count checking
- **Website Monitoring**: Check if websites are online or offline
- **RSS Feed Monitoring**: Automated Mindstar deal notifications with price tracking

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.10+** (required for match-case statements)
- **pip** (Python package manager)
- **Discord Bot Token** (from [Discord Developer Portal](https://discord.com/developers/applications))

### Required Python Packages

- `discord-py-interactions` - Discord bot framework
- `yfinance` - Yahoo Finance API wrapper
- `matplotlib` - Plotting library for stock charts
- `mcstatus` - Minecraft server status checker
- `feedparser` - RSS feed parser
- `numpy` - Numerical computing library
- `Pillow` - Image processing library
- `aiohttp` - Asynchronous HTTP client
- `schedule` - Task scheduling library

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/xniclaserdx/Discord_HexBot.git
   cd Discord_HexBot
   ```

2. **Install dependencies**
   ```bash
   pip install discord-py-interactions yfinance matplotlib mcstatus feedparser numpy Pillow aiohttp schedule
   ```

3. **Set up your bot token**
   
   Create a `TOKEN.txt` file in the `Bot` directory:
   ```bash
   cd Bot
   echo "YOUR_DISCORD_BOT_TOKEN_HERE" > TOKEN.txt
   ```

   > ⚠️ **Important**: Never commit your `TOKEN.txt` file to version control. It should be kept private.

## ⚙️ Configuration

1. **Create a Discord Bot**
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Click "New Application" and give it a name
   - Navigate to the "Bot" section and click "Add Bot"
   - Copy the bot token and save it in `Bot/TOKEN.txt`

2. **Set Bot Permissions**
   
   Your bot needs the following permissions:
   - Send Messages
   - Embed Links
   - Attach Files
   - Read Message History
   - Use Slash Commands

3. **Invite the Bot to Your Server**
   - In the Developer Portal, go to OAuth2 → URL Generator
   - Select scopes: `bot` and `applications.commands`
   - Select the permissions listed above
   - Use the generated URL to invite the bot to your server

## 💻 Usage

### Starting the Bot

Navigate to the `Bot` directory and run:

```bash
cd Bot
python bot.py
```

The bot will automatically:
- Load all extension modules
- Connect to Discord
- Display connected guilds and channels
- Start monitoring RSS feeds (if configured)

### Expected Output

```
extension loaded: basiscalc
extension loaded: finance_module
extension loaded: mc_server_status
extension loaded: website_check
extension loaded: matrixmodule
extension loaded: rss_mindstar
extensions loaded successfully
Logged in!
Bot is in 1 guild(s):
Logged in to YourServer (ID: 123456789)
```

## 📚 Commands Reference

All commands use Discord's slash command system. Type `/` in Discord to see available commands.

### Core Commands Module

| Command | Description | Parameters | Example |
|---------|-------------|------------|---------|
| `/hex_date` | Display the current date | None | `/hex_date` |
| `/hex_hi` | Friendly greeting | None | `/hex_hi` |
| `/hex_rng` | Random number generator | `lower_bound`, `upper_bound` | `/hex_rng lower_bound:1 upper_bound:100` |
| `/hex_coinflip` | Flip a coin | None | `/hex_coinflip` |

### Mathematical Operations

| Command | Description | Parameters | Example |
|---------|-------------|------------|---------|
| `/hex_base` | Convert decimal to other bases (2-36) | `number`, `base` | `/hex_base number:255 base:16` |
| `/hex_matrix` | Perform matrix calculations | `expression` | `/hex_matrix expression:(1,2;3,4) X (5,6;7,8)` |

**Matrix Command Syntax:**
- Matrices: `(row1_col1,row1_col2;row2_col1,row2_col2)`
- Operators: `+` (addition), `-` (subtraction), `X` (multiplication)
- Parentheses supported for operation ordering
- Spaces required between elements
- Example: `(1,2;3,4) + (5,6;7,8)` or `(1,0;0,1) X (2,3;4,5)`

### Finance Module

| Command | Description | Parameters | Example |
|---------|-------------|------------|---------|
| `/hex_stock_price` | Get current stock price | `ticker` | `/hex_stock_price ticker:AAPL` |
| `/hex_stock_plot` | Generate 2-year price chart | `ticker` | `/hex_stock_plot ticker:TSLA` |
| `/hex_stock_predict` | Predict stock trend using technical analysis | `ticker` | `/hex_stock_predict ticker:MSFT` |

**Stock Prediction Features:**
- 7-day and 20-day moving averages
- Momentum analysis (7-day price change)
- Volatility calculation
- Trend classification (Bullish, Bearish, or Neutral)
- Short-term prediction based on technical indicators

Supported tickers: Any valid Yahoo Finance ticker symbol (e.g., AAPL, GOOGL, MSFT, BTC-USD)

### Minecraft Server Status

| Command | Description | Parameters | Example |
|---------|-------------|------------|---------|
| `/mcstatus` | Check Minecraft server status | `server`, `port` (optional) | `/mcstatus server:mc.hypixel.net port:25565` |

Returns: Player count and server latency

### Website Monitoring

| Command | Description | Parameters | Example |
|---------|-------------|------------|---------|
| `/isoffline` | Check if a website is reachable | `url` | `/isoffline url:https://google.com` |

### RSS Feed Monitoring (Automated)

The bot automatically monitors the Mindstar RSS feed and posts deals that meet criteria:
- Discount > 10% OR
- Price difference > 50€

Messages are posted to channels named "mindstar" in your server.

## 📁 Project Structure

```
Discord_HexBot/
├── Bot/
│   ├── bot.py                 # Main bot file and entry point
│   ├── core_commands.py       # Basic utility commands
│   ├── basiscalc.py          # Base conversion module
│   ├── matrixmodule.py       # Matrix calculation module
│   ├── texmodule.py          # LaTeX rendering for math output
│   ├── finance_module.py     # Stock market data module
│   ├── mc_server_status.py   # Minecraft server checker
│   ├── website_check.py      # Website status checker
│   ├── rss_mindstar.py       # RSS feed monitoring
│   └── TOKEN.txt             # Your Discord bot token (not in git)
└── README.md                  # This file
```

### Module Descriptions

- **bot.py**: Main entry point that loads all extensions and handles bot initialization
- **core_commands.py**: Simple utility commands (date, greeting, RNG, coin flip)
- **basiscalc.py**: Converts decimal numbers to any base (2-36)
- **matrixmodule.py**: Advanced matrix operations with LaTeX-rendered output
- **texmodule.py**: Converts LaTeX expressions to PNG images via external API
- **finance_module.py**: Fetches stock data from Yahoo Finance and generates charts
- **mc_server_status.py**: Queries Minecraft servers using mcstatus library
- **website_check.py**: Simple HTTP availability checker
- **rss_mindstar.py**: Monitors Mindstar deals and auto-posts to Discord

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/YourFeature
   ```
3. **Make your changes**
   - Follow the existing code style
   - Add comments where necessary
   - Test your changes thoroughly
4. **Commit your changes**
   ```bash
   git commit -m "Add some feature"
   ```
5. **Push to the branch**
   ```bash
   git push origin feature/YourFeature
   ```
6. **Open a Pull Request**

### Code Guidelines

- Use meaningful variable and function names
- Follow PEP 8 style guidelines for Python
- Add docstrings to functions where appropriate
- Keep functions focused and modular
- Test commands before submitting

## 📄 License

This project is open source. Feel free to edit this code to fit your needs.

> **Note**: Some things may not be optimized perfectly. We welcome improvements!

## 👥 Authors

- **[@xniclaserdx](https://github.com/xniclaserdx)** - Co-creator and maintainer
- **[@ToreKnz](https://github.com/ToreKnz)** - Co-creator and contributor

## 🚧 Future Development

New features are currently in development! Stay tuned for updates.

### Planned Features
- Additional mathematical operations
- More financial data sources
- Extended monitoring capabilities
- Custom command configuration
- Database integration for persistent data

## 🙏 Acknowledgments

- Built with [discord-py-interactions](https://github.com/interactions-py/library)
- Stock data provided by [Yahoo Finance](https://finance.yahoo.com/)
- LaTeX rendering powered by [rtex](http://rtex.probablyaweb.site/) *(Note: Uses HTTP connection)*
- Minecraft server status via [mcstatus](https://github.com/py-mine/mcstatus)

## 📞 Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Ensure all dependencies are properly installed
- Verify your Discord bot token is correct

---

**Enjoy using Discord HexBot! 🎉**
