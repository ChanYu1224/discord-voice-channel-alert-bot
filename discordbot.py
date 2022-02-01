import discord
import datetime
import pytz
from os import getenv

TOKEN = getenv('DISCORD_BOT_TOKEN')
MESSAGE_ROOM = 937677135349440513

client = discord.Client()

def datetime_message():
    datetime_now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
    return str(datetime_now.year)+'/'+str(datetime_now.month)+'/'+str(datetime_now.day)+' '+str(datetime_now.hour)+':'+str(datetime_now.minute)+':'+str(datetime_now.second)

@client.event
async def on_voice_state_update(member:discord.Member, before, after):
    if before.channel != after.channel:
        message_room = client.get_channel(MESSAGE_ROOM)
        now_time = datetime_message()

        #enter alert
        if before.channel is None:
            message = member.name +' has joined to '+ after.channel.name +' at '+ now_time
            #print(message)
            await message_room.send(message)


        #exit alert
        elif after.channel is None:
            message = member.name +' has left '+ before.channel.name +' at '+ now_time
            #print(message)
            await message_room.send(message)

client.run(TOKEN)