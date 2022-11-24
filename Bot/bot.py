import discord
import random
import time
import datetime
import python_weather
import basiscalc
import numpy
import os
import mc_server_status

client = discord.Bot()
client = discord.Client(intents=discord.Intents.default())

token = "MTA0NTI5Nzk1NzQ2NzA2NjQyOA.G7XXPA.591eWjAryt2JgNuGoLZKMtBDk-djUHh4JOJTUY"

@client.event
async def on_ready():
    print("Logged in as a bot {0.user}".format(client))

@client.event
async def on_message(message):
    username = str(message.author).split("#")[0]
    channel = str(message.channel.name)
    user_message = str(message.content)

    user_message_stripped= user_message.strip().split(" ")
    user_message_stripped = list(filter(str.strip, user_message_stripped))  
  
    print(f'Message {user_message} by {username} on {channel}')
    print(user_message_stripped)
    if message.author == client.user:
        return

    if username!="HexBot":
        if channel == "test":
            if user_message_stripped[0]=="!hex" or user_message_stripped[0]=="/hex" or user_message_stripped[0]=="\hex":
                if user_message_stripped[1]=="date":
                    today = datetime.datetime.today()
                    await message.channel.send(f"{today:%B %d, %Y}")
                elif user_message_stripped[1]=="base" and user_message_stripped[3]=="to":
                    await message.channel.send(basiscalc.basis(user_message_stripped[2],user_message_stripped[4]))
                elif user_message_stripped[1].lower()=="hi":
                    await message.channel.send(f"Hallo, {username} <3")
                elif user_message_stripped[1].lower()=="rng" and user_message_stripped[3].lower()=="to":
                    await message.channel.send(str(random.randint(int(user_message_stripped[2]),int(user_message_stripped[4]))))
                elif user_message_stripped[1].lower()=="coinflip" or user_message_stripped[1].lower()=="Münzwurf":
                    await message.channel.send("Kopf" if random.randint(0,1)==1 else "Zahl")
                elif user_message_stripped[1].lower()=="mc" and user_message_stripped[2].lower()=="status":
                    await message.channel.send(mc_server_status.return_server_status(str(user_message_stripped[3]), int(user_message_stripped[4])))
                return

client.run(token)
