"""Core command module for basic Discord bot utilities."""
import interactions
import random
import datetime


class CoreModule(interactions.Extension):
    """Extension module for core bot commands."""
    
    def __init__(self, client):
        self.client = client

    @interactions.extension_command(
        name="hex_date",
        description="Prints the current date"
    )
    async def date_command(self, ctx: interactions.CommandContext):
        """Display the current date."""
        today = datetime.datetime.today()
        await ctx.send(f"{today:%B %d, %Y}")

    @interactions.extension_command(
        name="hex_hi",
        description="A friendly greeting"
    )
    async def hi_command(self, ctx: interactions.CommandContext):
        """Send a friendly greeting to the user."""
        await ctx.send(f"Hello, {ctx.user} <3")

    @interactions.extension_command(
        name="hex_rng",
        description="picks a random integer number between two specified integers",
        options=[
            interactions.Option(
                name="lower_bound",
                description="lower bound for chosen number",
                type=interactions.OptionType.INTEGER,
                required=True,
            ),
            interactions.Option(
                name="upper_bound",
                description="upper bound for chosen number",
                type=interactions.OptionType.INTEGER,
                required=True,
            )
        ]
    )
    async def rng_command(self, ctx: interactions.CommandContext, lower_bound: int, upper_bound: int):
        """Generate a random number between the specified bounds."""
        await ctx.send(str(random.randint(lower_bound, upper_bound)))

    @interactions.extension_command(
        name="hex_coinflip",
        description="Flips a coin"
    )
    async def coinflip_command(self, ctx: interactions.CommandContext):
        """Flip a coin and return the result."""
        result = "Heads" if random.randint(0, 1) == 1 else "Tails"
        await ctx.send(result)


def setup(client):
    """Set up the CoreModule extension."""
    CoreModule(client)