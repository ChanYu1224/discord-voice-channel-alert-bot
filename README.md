# Introduction
## What is this bot?
Discord voice channel alert bot is a very useful bot for working people on discord. When you set this bot to your discord channel, the teamwork and productivity of your group increases so much.
### Alert of Voice Channel State
This bot alerts entering to voice channel and exiting from voice channel.
```
<user display name> has entered to <voice channel name>
<user display name> has exited from <voice channel name>
```

### Alert of Working Times
This bot alerts how long you stayed on voice channel weekly and daily.
```
[ weekly working times ]
Tom            018H33M
Hanako         011H04M
...
```
```
[ daily working times ]
Tom            002H30M
Hanako         001H49M
...
```

## Usage
### Recommended Environment
- Python 3.10.8
- Ubuntu 22.04

### Installation
```
git clone https://github.com/ChanYu1224/discord-voice-channel-alert-bot.git
cd ./discord-voice-channel-alert-bot
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Settings
Execute the following command 

```
touch settings.json
```

and edit `settings.json`

```json
{
    // discord bot token (required)
    "token": "********",
    // you have to specify the room post alerts (required)
    "message_room_id": 1234567890,
    // if you specify `true`, alerts of working time are enabled
    "is_enable_working_time_alert": true,
    // language of alerts, "en" or "ja"
    "lang": "ja",
    // you can specify working rooms.
    "working_room_ids": [
        10987654321,
        90123456789,
    ],
    // when the bot alerts working time (Mon. = 0, Tue. = 1 ...)
    "weekly_alert_weekday": 0,
    "weekly_alert_time": "21:00",
    "daily_alert_time": "21:00"
}
```
You can configure the discord bot and get the `"token"` from [here](https://discord.com/developers/applications). And to get the `"message_room_id"`, run bellow:

```
python get_room_id.py
```

### Run
```
python discordbot.py
```