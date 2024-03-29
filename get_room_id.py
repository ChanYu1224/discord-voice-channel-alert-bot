import discord
import json

intents = discord.Intents.all()
client = discord.Client(intents=intents)

with open("./settings.json", mode="r") as setting_file:
    setting_dict = json.load(setting_file)

TOKEN = setting_dict["token"]

@client.event
async def on_ready():
    for channel in client.get_all_channels():
        print("---------------")
        print("channel name", str(channel.name))
        print("channel ID", str(channel.id))
    print("---------------")

client.run(TOKEN)