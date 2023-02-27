import feedparser
import time
import interactions

class RSS_mindstarModule(interactions.Extension):
    def __init__(self,client):
        self.client = client

    async def check_prices(self,client):
        feed_url = "https://www.mindfactory.de/xml/rss/mindstar_artikel.xml"
        feed = feedparser.parse(feed_url)
        for item in feed["items"]:
            time.sleep(3)
            price = float(item["_price"].replace(".", "").replace(",", "."))/100
            msprice = float(item["_msprice"].replace(".", "").replace(",", "."))/100
            discount = round(((price - msprice) / price) * 100, 2)
            if discount > 10 or price-msprice>50:
                message = item["title"] + "\n" + item["link"] + "\n" + "Regulärer Preis:     " + item["_price"] + "€" + "\n" + "Mindstar-Preis:      " + item["_msprice"] + "€" + "\n"
                message += f"Nachlass um: {discount}%"
                for guild in client.guilds:
                        for channel in await guild.get_all_channels():
                            if str(channel)=="mindstar":
                                await channel.send(message)
        
def setup(client):
    RSS_mindstarModule(client)

