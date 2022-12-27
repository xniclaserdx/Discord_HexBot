# import discord
import random
import time
import datetime
import python_weather
import basiscalc
import numpy
import finance_module
import os
import mc_server_status
import website_check
import matrixmodule
import io
import interactions
from interactions.ext.files import command_send

text_file = open(os.path.dirname(os.path.abspath(__file__))+"/TOKEN.txt", "r")
token = text_file.read()
text_file.close()
client = interactions.Client(token=token)
client.load('interactions.ext.files')

# successful start
@client.event
async def on_ready():
    #print("Logged in as a bot {0.user}".format(client))
    print('Logged in successfully')

# hex keyword for commands
@client.command(
    name = "hex"
)
async def hex_commands(ctx: interactions.CommandContext):
    pass



# command for date
@hex_commands.subcommand(
    name = "date",
    description = "Prints the current date"
)
async def date_command(ctx: interactions.CommandContext):
    today = datetime.datetime.today()
    await ctx.send(f"{today:%B %d, %Y}")



# command for basecalc
@hex_commands.subcommand(
    name = "base",
    description = "Converts decimal numbers to numbers of other bases",
    options = [
        interactions.Option(
            name = "number",
            description = "number you want to convert",
            type = interactions.OptionType.INTEGER,
            required = True,
        ),
        interactions.Option(
            name = "base",
            description = "base you want to convert to",
            type = interactions.OptionType.INTEGER,
            required = True,
        )
    ]
)
async def basecalc_command(ctx: interactions.CommandContext,number: int, base: int):
    await ctx.send(basiscalc.basis(number,base))



# command for greeting
@hex_commands.subcommand(
    name = "hi",
    description = "A friendly greeting"
)
async def hi_command(ctx: interactions.CommandContext):
    await ctx.send(f"Hallo, {ctx.user} <3")



# command for rng
@hex_commands.subcommand(
    name = "rng",
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
@hex_commands.subcommand(
    name = "coinflip",
    description = "Flips a coin"
)
async def coinflip_command(ctx: interactions.CommandContext):
    await ctx.send("Kopf" if random.randint(0,1)==1 else "Zahl")



# command for mc server status check
@hex_commands.subcommand(
    name = "mcstatus",
    description = "Checks the status of a minecraft server",
    options = [
        interactions.Option(
            name = "server",
            description = "Minecraft server to be checked",
            type = interactions.OptionType.STRING,
            required = True,
        ),
        interactions.Option(
            name = "port",
            description = "Port (hab kein Plan wofür der ist, gerne ergänzen)",
            type = interactions.OptionType.INTEGER,
            required = False,
        )
    ]
)
async def mcstatus_command(ctx: interactions.CommandContext,server: str, port: int = 25565):
    await ctx.send(mc_server_status.return_server_status(server,port))



# command to check if websites are online
@hex_commands.subcommand(
    name = "isoffline",
    description = "Checks if a website is offline",
    options = [
        interactions.Option(
            name = "website",
            description = "Website to be checked",
            type = interactions.OptionType.STRING,
            required = True
        )
    ]
)
async def isoffline_command(ctx: interactions.CommandContext, website: str):
    await ctx.send(website_check.checkSite(website))



# command to get stock values
@hex_commands.subcommand(
    name ="finance_price",
    description = "Checks the value of a stock (?); to be updated",
    options = [
        interactions.Option(
            name = "stock",
            description = "Stock name",
            type = interactions.OptionType.STRING,
            required = True
        )
    ]
)
async def finance_price_command(ctx: interactions.CommandContext, stock: str):
    await ctx.send(finance_module.get_market_price(stock))



# command for matrix calculations
@hex_commands.subcommand(
    name = "matrix",
    description = "Can perfom multiple matrix operations",
    options = [
        interactions.Option(
            name = "expression",
            description = "expression to be evaluated, matrix format: (1,2;3,4), spaces between inputs needed",
            type = interactions.OptionType.STRING,
            required = True
        )
    ]
)
async def matrix_command(ctx: interactions.CommandContext, expression: str):
    expression_args = expression.split(" ")
    image = await matrixmodule.mathInputEvaluate(expression_args)
    imageByteArr = io.BytesIO()
    image.save(imageByteArr,format='PNG')
    imageByteArr.seek(0)
    # await ctx.send(interactions.File(filename = "response.png",fp = image)) # muss ich noch anpassen!!
    #await ctx.send("yo das hier klappt mehr oder weniger")
    await command_send(ctx,"",files = interactions.File(fp = imageByteArr,filename="response.png"))

client.start()