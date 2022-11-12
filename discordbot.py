import discord
from discord.ext import tasks

import json
from os import getenv
import os
import datetime

from working_time import WorkingRecords

# if `dev_settings.json` exists, read it
if os.path.exists("./dev_settings.json"):
    with open("./dev_settings.json", mode="r") as setting_file:
        setting_dict = json.load(setting_file)
    TOKEN = setting_dict["DISCORD_BOT_TOKEN"]
    MESSAGE_ROOM = int(setting_dict["DISCORD_MESSAGE_ROOM"])
    WORKING_ROOMS = list(map(int, setting_dict["DISCORD_WORKING_ROOMS"].split(",")))
    WEEKLY_ALERT_DAY = int(setting_dict["DISCORD_WEEKLY_ALERT_DAY"])
    WEEKLY_ALERT_TIME = setting_dict["DISCORD_WEEKLY_ALERT_TIME"]
    DAILY_ALERT_TIME = setting_dict["DISCORD_DAILY_ALERT_TIME"]
else:
    TOKEN = getenv('DISCORD_BOT_TOKEN')
    MESSAGE_ROOM = int(getenv('DISCORD_MESSAGE_ROOM'))
    WORKING_ROOMS = list(map(int, getenv("DISCORD_WORKING_ROOMS").split(",")))
    WEEKLY_ALERT_DAY = int(getenv("DISCORD_WEEKLY_ALERT_DAY"))
    WEEKLY_ALERT_TIME = getenv("DISCORD_WEEKLY_ALERT_TIME")
    DAILY_ALERT_TIME = getenv("DISCORD_DAILY_ALERT_TIME")
    
# initialization of necessary instances
intents = discord.Intents.all()
client = discord.Client(intents=intents)

weekly_records = WorkingRecords()
daily_records = WorkingRecords()
message_room = None


@client.event
async def on_ready():
    global message_room
    message_room = client.get_channel(MESSAGE_ROOM)
    show_working_times.start()
    await message_room.send(client.user.display_name +"が起動しました")


# alert of working time
@tasks.loop(seconds=60)
async def show_working_times():
    date = datetime.date.today()
    now_time = datetime.datetime.now()
    now = now_time.strftime("%H:%M")
    
    # weekly alert
    if date.weekday() == WEEKLY_ALERT_DAY and now == WEEKLY_ALERT_TIME:
        # the header of the message
        message = "【今週の作業時間】\n"
        message += weekly_records.get_sorted_working_records()
        
        weekly_records.reset_records()
        
        await message_room.send(message)
    
    # daily alert
    if now == DAILY_ALERT_TIME:
        # the header of the message
        message = "【今日の作業時間】\n"
        message += daily_records.get_sorted_working_records()
        
        daily_records.reset_records()
            
        await message_room.send(message)
        

# alert of enter and exit
@client.event
async def on_voice_state_update(
        member:discord.Member,
        before:discord.VoiceState,
        after:discord.VoiceState
    ):
    # when bots activate this method, it does nothing
    if "bot" in list(map(str, member.roles)):
        return
    
    if before.channel != after.channel:
        member_name = member.display_name

        # enter alert
        if before.channel is None:
            # update the state of working time
            if after.channel.id in WORKING_ROOMS:
                weekly_records.start_record(member_name)
                daily_records.start_record(member_name)
            
            message = member_name +'が'+ after.channel.name +'に入室'
            await message_room.send(message)

        # exit alert
        elif after.channel is None:
            # update the state of working time
            weekly_records.stop_record(member_name)
            daily_records.stop_record(member_name)
            
            message = member_name +'が'+ before.channel.name +'を退室'
            await message_room.send(message)
        
        # change the room
        else:
            # update the state of working time
            if before.channel.id in WORKING_ROOMS and not after.channel.id in WORKING_ROOMS:
                # move from working room
                weekly_records.stop_record(member_name)
                daily_records.stop_record(member_name)
                        
            elif not before.channel.id in WORKING_ROOMS and after.channel.id in WORKING_ROOMS:
                # move to working room
                weekly_records.start_record(member_name)
                daily_records.start_record(member_name)
            
            message = member_name +'が'+ after.channel.name +'に移動'
            await message_room.send(message)
            
            
client.run(TOKEN)