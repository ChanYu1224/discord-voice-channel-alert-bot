import discord
from discord.ext import tasks

import logging
import pprint
import json
import os
import datetime

from modules import WorkingRecords

# set the logging
logger = logging.getLogger("discordbot logger")
logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
file_handler = logging.FileHandler("discordbot.log", encoding="utf-8", mode="w")
logger.addHandler(file_handler)

formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# if `settings.json` exists, read it
if os.path.exists("./settings.json"):
    with open("./settings.json", mode="r") as setting_file:
        settings:dict = json.load(setting_file)
    
    # catch the exception by assertion
    assert "token" in settings.keys()
    assert "message_room_id" in settings.keys()
    
    # set the default values
    settings["is_enable_working_time_alert"] = settings.get("is_enable_working_time_alert", False)
    settings["weekly_alert_weekday"] = settings.get("weekly_alert_weekday", 0)
    settings["weekly_alert_time"] = settings.get("weekly_alert_time", "21:00")
    settings["daily_alert_time"] = settings.get("daily_alert_time", "21:00")
    
    if "lang" in settings.keys():
        if not settings["lang"] in ["ja", "en"]:
            raise ValueError("{0} is not supported as language".format(settings["lang"]))
    else:
        settings["lang"] = "en"
    
    logger.info("initialized by setting as folows:\n{}".format(pprint.pformat(settings, indent=4)))
else:
    raise FileNotFoundError("`settings.json` does not exist")


# initialization of necessary instances
intents = discord.Intents.all()
client = discord.Client(intents=intents)

weekly_records = WorkingRecords()
daily_records = WorkingRecords()
message_room = None


@client.event
async def on_ready():
    # set the message room
    global message_room
    message_room = client.get_channel(settings["message_room_id"])
    
    # the setting for working time alert
    if settings["is_enable_working_time_alert"]:
        # initialization of user states
        for working_room_id in settings["working_room_ids"]:
            working_voice_channel = client.get_channel(working_room_id)
            for member_id in working_voice_channel.voice_states.keys():
                member = await client.fetch_user(member_id)
                weekly_records.start_record(member)
                daily_records.start_record(member)
                logger.info("{0} has already entered into working room".format(member.display_name))
        
        # initialization of working time alert
        show_working_times.start()
        logger.info("discord bot is activated!")
    
    # send activation message
    if settings["lang"] == "ja":
        await message_room.send(client.user.display_name +"が起動しました")
    else:
        await message_room.send(client.user.display_name +" is now activated")


# alert of working time
@tasks.loop(seconds=60)
async def show_working_times():
    date = datetime.date.today()
    now_time = datetime.datetime.now()
    now = now_time.strftime("%H:%M")
    
    # weekly alert
    if date.weekday() == settings["weekly_alert_weekday"] and now == settings["weekly_alert_time"]:
        # the header of the message
        if settings["lang"] == "ja":
            message = "【今週の作業時間】\n"
        else:
            message = "[ weekly working times ]\n"
        
        message += weekly_records.get_sorted_working_records()
        
        weekly_records.reset_records()
        
        await message_room.send(message)
    
    # daily alert
    if now == settings["daily_alert_time"]:
        # the header of the message
        if settings["lang"] == "ja":
            message = "【今日の作業時間】\n"
        else:
            message = "[ today's working times ]\n"
        
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
    member_roles_list = list(map(str, member.roles))
    if "bot" in member_roles_list:
        return
    
    if before.channel != after.channel:
        # enter alert
        if before.channel is None:
            # update the state of working time
            if after.channel.id in settings["working_room_ids"]:
                weekly_records.start_record(member)
                daily_records.start_record(member)
            
            if settings["lang"] == "ja":
                message = member.display_name +'が'+ after.channel.name +'に入室'
            else:
                message = "{0} has entered to {1}".format(member.display_name, after.channel.name)
            
            logger.info(message)
            await message_room.send(message)

        # exit alert
        elif after.channel is None:
            # update the state of working time
            weekly_records.stop_record(member)
            daily_records.stop_record(member)
            
            if settings["lang"] == "ja":
                message = member.display_name +'が'+ before.channel.name +'を退室'
            else:
                message = "{0} has exited from {1}".format(member.display_name, before.channel.name)
            
            logger.info(message)
            await message_room.send(message)
        
        # change the room
        else:
            # update the state of working time
            if before.channel.id in settings["working_room_ids"] and not after.channel.id in settings["working_room_ids"]:
                # move from working room
                weekly_records.stop_record(member)
                daily_records.stop_record(member)
                
            elif not before.channel.id in settings["working_room_ids"] and after.channel.id in settings["working_room_ids"]:
                # move to working room
                weekly_records.start_record(member)
                daily_records.start_record(member)
            
            if settings["lang"] == "ja":
                message = member.display_name +'が'+ after.channel.name +'に移動'
            else:
                message = "{0} has moved to {1}".format(member.display_name, after.channel.name)
            
            logger.info(message)
            await message_room.send(message)
            
            

client.run(settings["token"])