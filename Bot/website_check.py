"""Module for checking website availability."""
import urllib.request
import urllib.error
import interactions


def check_site(site: str) -> str:
    """
    Check if a website is reachable.
    
    Args:
        site: Full URL of the website to check
        
    Returns:
        String indicating whether the site is online or not
    """
    try:
        response = urllib.request.urlopen(str(site), timeout=10)
        if response.getcode() == 200:
            return "Site is online"
        return f"Site returned status code: {response.getcode()}"
    except urllib.error.HTTPError as e:
        return f"Site returned HTTP error: {e.code}"
    except urllib.error.URLError as e:
        return f"Site not reachable: {e.reason}"
    except TimeoutError:
        return "Site request timed out..."
    except Exception as e:
        return f"Error checking site: {type(e).__name__}"


class WebsiteCheckModule(interactions.Extension):
    """Extension module for website availability checking."""
    
    def __init__(self, client):
        self.client = client

    @interactions.extension_command(
        name="isoffline",
        description="Checks if a website is offline",
        options=[
            interactions.Option(
                name="url",
                description="Full url of the website to be checked",
                type=interactions.OptionType.STRING,
                required=True
            )
        ]
    )     
    async def isoffline_command(self, ctx: interactions.CommandContext, url: str):
        """Handle website availability check command."""
        await ctx.send(check_site(url))


def setup(client):
    """Set up the WebsiteCheckModule extension."""
    WebsiteCheckModule(client)
