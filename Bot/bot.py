"""Main bot entry point for Discord HexBot."""
import os
import interactions
import schedule
import time

def _get_extensions():
    """Get list of extension modules to load."""
    yield 'basiscalc'
    yield 'finance_module'
    yield 'mc_server_status'
    yield 'website_check'
    yield 'matrixmodule'
    yield 'rss_mindstar'


# Read bot token from file using context manager
token_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "TOKEN.txt")
with open(token_path, "r", encoding="utf-8") as text_file:
    token = text_file.read().strip()

client = interactions.Client(token=token)
client.load('interactions.ext.files')
client.load('core_commands')

for i in _get_extensions():
    client.load(i)
    print("extension loaded: "+ i)
print("extensions loaded successfully")

@client.event
async def on_ready():
    """Handle bot ready event and start RSS monitoring."""
    print("Logged in!")
    print(f"Bot is in {len(client.guilds)} guild(s):")
    for guild in client.guilds:
        print(f'Logged in to {guild.name} (ID: {guild.id})')
        for channel in await guild.get_all_channels():
            print(f'Channel {channel}')
    
    # Start RSS monitoring once
    await client._extensions["RSS_mindstarModule"].check_prices(client)

client.start()