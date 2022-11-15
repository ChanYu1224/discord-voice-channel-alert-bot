import discord
from discord.ext import tasks

import json
import os
import datetime

from working_time import WorkingRecords


# if `settings.json` exists, read it
if os.path.exists("./settings.json"):
    with open("./settings.json", mode="r") as setting_file:
        settings = json.load(setting_file)
    
    # catch the exception by assertion
    assert settings["token"] is not None
    assert settings["message_room_id"] is not None
    assert settings["is_enable_working_time_alert"] is not None
else:
    raise FileNotFoundError("`settings.json` does not exist.")


# initialization of necessary instances
intents = discord.Intents.all()
client = discord.Client(intents=intents)

weekly_records = WorkingRecords()
daily_records = WorkingRecords()
message_room = None


@client.event
async def on_ready():
    global message_room
    message_room = client.get_channel(settings["message_room_id"])
    if settings["is_enable_working_time_alert"]:
        show_working_times.start()
    await message_room.send(client.user.display_name +"が起動しました")


# alert of working time
@tasks.loop(seconds=60)
async def show_working_times():
    date = datetime.date.today()
    now_time = datetime.datetime.now()
    now = now_time.strftime("%H:%M")
    
    # weekly alert
    if date.weekday() == settings["weekly_alert_weekday"] and now == settings["weekly_alert_time"]:
        # the header of the message
        message = "【今週の作業時間】\n"
        message += weekly_records.get_sorted_working_records()
        
        weekly_records.reset_records()
        
        await message_room.send(message)
    
    # daily alert
    if now == settings["daily_alert_time"]:
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
            if after.channel.id in settings["working_room_ids"]:
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
            if before.channel.id in settings["working_room_ids"] and not after.channel.id in settings["working_room_ids"]:
                # move from working room
                weekly_records.stop_record(member_name)
                daily_records.stop_record(member_name)
                        
            elif not before.channel.id in settings["working_room_ids"] and after.channel.id in settings["working_room_ids"]:
                # move to working room
                weekly_records.start_record(member_name)
                daily_records.start_record(member_name)
            
            message = member_name +'が'+ after.channel.name +'に移動'
            await message_room.send(message)
            
            
client.run(settings["token"])