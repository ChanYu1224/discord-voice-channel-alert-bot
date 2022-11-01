import discord
from discord.ext import tasks

import json
from os import getenv
import datetime

from working_time import WorkingTime

# specify the mode, debugging or real environemnt
debug = False
if debug:
    with open("./dev_settings.json", mode="r") as setting_file:
        setting_dict = json.load(setting_file)
    TOKEN = setting_dict["TOKEN"]
    MESSAGE_ROOM = int(setting_dict["CHANNNEL_ID"])
else:
    TOKEN = getenv('DISCORD_BOT_TOKEN')
    MESSAGE_ROOM = int(getenv('DISCORD_MESSAGE_ROOM'))

# initiation of necessary instances
intents = discord.Intents.all()
client = discord.Client(intents=intents)
working_time_dict = {}

# alert of working time
@tasks.loop(seconds=60)
async def show_working_times():
    date = datetime.date.today()
    now_time = datetime.datetime.now()
    now = now_time.strftime("%H:%M")
    
    if date.weekday() == 0 and now == "21:00":
        # the header of the message
        message = "今週の作業時間\n"
        for member_name, working_time in working_time_dict.items():
            # make the annotation for `working_time`
            working_time: WorkingTime = working_time
            
            # if you are working now, it resets the working time ongoing
            if working_time.is_working():
                working_time.end_working()
                working_time.start_working()
            
            # create the message explainging the total working time
            message += "{0} : {1}\n".format(member_name, working_time)
            
            # reset the working time weekly
            working_time.reset_working_time()
            
        message_room = client.get_channel(MESSAGE_ROOM)
        await message_room.send(message)


# alert of enter and exit
@client.event
async def on_voice_state_update(member:discord.Member, before, after):
    if before.channel != after.channel:
        message_room = client.get_channel(MESSAGE_ROOM)
        member_name = member.display_name
        now_time = datetime.datetime.now()

        # enter alert
        if before.channel is None:
            message = member_name +'が'+ after.channel.name +'に入室'
            
            # update the state of working time
            if not member_name in working_time_dict.keys():
                working_time_dict[member_name] = WorkingTime(now_time)
            working_time: WorkingTime = working_time_dict[member_name]
            working_time.start_working()
            
            await message_room.send(message)

        # exit alert
        elif after.channel is None:
            message = member_name +'が'+ before.channel.name +'を退室'
            
            # update the state of working time
            if member_name in working_time_dict.keys():
                working_time: WorkingTime = working_time_dict[member_name]
                if working_time.is_working():
                    working_time.end_working()

            await message_room.send(message)

show_working_times.start()
client.run(TOKEN)