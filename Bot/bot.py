import os
import interactions
import schedule
import time

def _get_extensions():
    yield 'basiscalc'
    yield 'finance_module'
    yield 'mc_server_status'
    yield 'website_check'
    yield 'matrixmodule'
    yield 'rss_mindstar'


text_file = open(os.path.dirname(os.path.abspath(__file__))+"/TOKEN.txt", "r")
token = text_file.read()
text_file.close()
client = interactions.Client(token=token)
client.load('interactions.ext.files')
client.load('core_commands')

for i in _get_extensions():
    client.load(i)
    print("extension loaded: "+ i)
print("extensions loaded successfully")

@client.event
async def on_ready():
    print(f"Logged in!")
    print(f"Bot is in {len(client.guilds)} guild(s):")
    for guild in client.guilds:
        print(f'Logged in to {guild.name} (ID: {guild.id})')
        for channel in await guild.get_all_channels():
            print(f'Channel {channel}')
    # schedule.every().day.at("21:10").do(check_prices)

    await client._extensions["RSS_mindstarModule"].check_prices(client)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

client.start()