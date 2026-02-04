"""Module for monitoring Mindstar RSS feed for deals."""
import feedparser
import time
import interactions


class RSS_mindstarModule(interactions.Extension):
    """Extension module for RSS feed monitoring."""
    
    def __init__(self, client):
        self.client = client

    async def check_prices(self, client):
        """
        Check Mindstar RSS feed for deals and post to Discord.
        
        Posts deals that have >10% discount or >50€ price difference.
        
        Args:
            client: Discord client instance
        """
        feed_url = "https://www.mindfactory.de/xml/rss/mindstar_artikel.xml"
        
        try:
            feed = feedparser.parse(feed_url)
            
            if not feed.get("items"):
                print("No items found in RSS feed")
                return
                
            for item in feed["items"]:
                try:
                    time.sleep(3)  # Rate limiting
                    
                    # Parse prices
                    price = float(item["_price"].replace(".", "").replace(",", ".")) / 100
                    msprice = float(item["_msprice"].replace(".", "").replace(",", ".")) / 100
                    discount = round(((price - msprice) / price) * 100, 2)
                    
                    # Check if deal meets criteria
                    if discount > 10 or price - msprice > 50:
                        message = (
                            f"{item['title']}\n"
                            f"{item['link']}\n"
                            f"Regular Price:     {item['_price']}€\n"
                            f"Mindstar Price:    {item['_msprice']}€\n"
                            f"Discount: {discount}%"
                        )
                        
                        # Post to all 'mindstar' channels
                        for guild in client.guilds:
                            for channel in await guild.get_all_channels():
                                if str(channel) == "mindstar":
                                    await channel.send(message)
                except (KeyError, ValueError) as e:
                    print(f"Error processing RSS item: {e}")
                    continue
                except Exception as e:
                    print(f"Unexpected error processing RSS item: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error fetching RSS feed: {e}")

        
def setup(client):
    """Set up the RSS_mindstarModule extension."""
    RSS_mindstarModule(client)

