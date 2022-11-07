import discord
from discord.ext import tasks

import json
from os import getenv
import os
import datetime

from working_time import WorkingTime

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
working_time_dict = {}

# alert of working time
@tasks.loop(seconds=60)
async def show_working_times():
    date = datetime.date.today()
    now_time = datetime.datetime.now()
    now = now_time.strftime("%H:%M")
    
    # weekly alert
    if date.weekday() == WEEKLY_ALERT_DAY and now == WEEKLY_ALERT_TIME:
        # the header of the message
        message = "今週の作業時間\n"
        for member_name, working_time in working_time_dict.items():
            # make the annotation for `working_time`
            working_time: WorkingTime = working_time
            
            # if you are working now, it resets the working time ongoing
            if working_time.is_working():
                working_time.end_working()
                working_time.start_working()
            
            # create the message explaining the total working time
            message += "{0}\t{1}\n".format(member_name, working_time.get_weekly_working_time_str())
            
            # reset the working time weekly
            working_time.reset_weekly_working_time()
            
        message_room = client.get_channel(MESSAGE_ROOM)
        await message_room.send(message)
    
    # daily alert
    if now == DAILY_ALERT_TIME:
        # the header of the message
        message = "今日の作業時間\n"
        for member_name, working_time in working_time_dict.items():
            # make the annotation for `working_time`
            working_time: WorkingTime = working_time
            
            # if you are working now, it resets the working time ongoing
            if working_time.is_working():
                working_time.end_working()
                working_time.start_working()
            
            # create the message explaining the total working time
            message += "{0}\t{1}\n".format(member_name, working_time.get_daily_working_time_str())

            # reset the working time daily
            working_time.reset_daily_working_time()
            
        message_room = client.get_channel(MESSAGE_ROOM)
        await message_room.send(message)
        

# alert of enter and exit
@client.event
async def on_voice_state_update(
        member:discord.Member,
        before:discord.VoiceState,
        after:discord.VoiceState
    ):
    if before.channel != after.channel:
        message_room = client.get_channel(MESSAGE_ROOM)
        member_name = member.display_name
        now_time = datetime.datetime.now()

        # enter alert
        if before.channel is None:
            # update the state of working time
            if after.channel.id in WORKING_ROOMS:                
                if not member_name in working_time_dict.keys():
                    working_time_dict[member_name] = WorkingTime(now_time)
                working_time: WorkingTime = working_time_dict[member_name]
                working_time.start_working()
            
            message = member_name +'が'+ after.channel.name +'に入室'
            await message_room.send(message)

        # exit alert
        elif after.channel is None:
            # update the state of working time
            if member_name in working_time_dict.keys():
                working_time: WorkingTime = working_time_dict[member_name]
                if working_time.is_working():
                    working_time.end_working()
            
            message = member_name +'が'+ before.channel.name +'を退室'
            await message_room.send(message)
        
        # change the room
        else:
            # update the state of working time
            if before.channel.id in WORKING_ROOMS and not after.channel.id in WORKING_ROOMS:
                # move from working room
                if member_name in working_time_dict.keys():
                    working_time: WorkingTime = working_time_dict[member_name]
                    if working_time.is_working():
                        working_time.end_working()
                        
            elif not before.channel.id in WORKING_ROOMS and after.channel.id in WORKING_ROOMS:
                # move to working room
                if not member_name in working_time_dict.keys():
                    working_time_dict[member_name] = WorkingTime(now_time)
                working_time: WorkingTime = working_time_dict[member_name]
                working_time.start_working()
            
            message = member_name +'が'+ after.channel.name +'に移動'
            await message_room.send(message)
            

show_working_times.start()
client.run(TOKEN)