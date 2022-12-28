import interactions
import random
import datetime

class CoreModule(interactions.Extension):
    def __init__(self,client):
        self.client = client

    # command for date
    @interactions.extension_command(
        name = "hex_date",
        description = "Prints the current date"
    )
    async def date_command(ctx: interactions.CommandContext):
        today = datetime.datetime.today()
        await ctx.send(f"{today:%B %d, %Y}")


    # command for greeting
    @interactions.extension_command(
        name = "hex_hi",
        description = "A friendly greeting"
    )
    async def hi_command(ctx: interactions.CommandContext):
        await ctx.send(f"Hallo, {ctx.user} <3")

    # command for rng
    @interactions.extension_command(
        name = "hex_rng",
        description = "picks a random integer number between two specified integers",
        options = [
            interactions.Option(
                name = "lower_bound",
                description = "lower bound for chosen number",
                type = interactions.OptionType.INTEGER,
                required = True,
            ),
            interactions.Option(
                name = "upper_bound",
                description = "upper bound for chosen number",
                type = interactions.OptionType.INTEGER,
                required = True,
            )
        ]
    )
    async def rng_command(ctx: interactions.CommandContext,lower_bound: int, upper_bound: int):
        await ctx.send(str(random.randint(lower_bound,upper_bound)))

    # command for coinflip
    @interactions.extension_command(
        name = "coinflip",
        description = "Flips a coin"
    )
    async def coinflip_command(ctx: interactions.CommandContext):
        await ctx.send("Kopf" if random.randint(0,1)==1 else "Zahl")

def setup(client):
    CoreModule(client)