import urllib.request
import interactions

def checkSite(site):
    try:
        urllib.request.urlopen(str(site)).getcode()==200 
        return "Site online" 
    except: 
        return "Site not reachable..."

class WebsiteCheckModule(interactions.Extension):
    def __init__(self,client):
        self.client = client

    # command to check if websites are online
    @interactions.extension_command(
        name = "isoffline",
        description = "Checks if a website is offline",
        options = [
            interactions.Option(
                name = "url",
                description = "Full url of the website to be checked",
                type = interactions.OptionType.STRING,
                required = True
            )
        ]
    )     
    async def isoffline_command(self,ctx: interactions.CommandContext, website: str):
        await ctx.send(checkSite(website))

def setup(client):
    WebsiteCheckModule(client)
