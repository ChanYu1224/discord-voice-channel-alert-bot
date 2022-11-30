# 日本語ドキュメント
このdiscord botは、ボイスチャンネルアラートボットであり、discordを用いて作業をしている人々にとって非常に有用なものです。もし、あなたがこのdiscord botをチャンネルに招待すれば、チームワークや生産性が上がること間違いなしです。もちろん、作業だけではなく、ゲームサーバにも非常に有用です。

### ボイスチャンネルの状態を通知
ボイスチャンネルに誰かが入ったり、ボイスチャンネルから誰かが出て行ったりした場合に通知を指定したテキストチャンネルに送信します。
```
<user display name>が<voice channel name>に入室
<user display name>が<voice channel name>を退室
```

### 作業時間を通知
誰がどのくらいの時間ボイスチャンネルで作業を行なったかを通知することが出来ます。
週毎、もしくは日毎、もしくは両方の作業時間を通知します。
```
【今週の作業時間】
Tom            018H33M
Hanako         011H04M
...
```
```
【今日の作業時間】
Tom            002H30M
Hanako         001H49M
...
```

## 使い方
### 推奨環境
- Python 3.10.8
- Ubuntu 22.04

### インストール
```
git clone https://github.com/ChanYu1224/discord-voice-channel-alert-bot.git
cd ./discord-voice-channel-alert-bot
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 設定
以下のコマンドを実行して、

```
touch settings.json
```

`settings.json`を編集します。

```jsonc
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
`"token"`は[ここ](https://discord.com/developers/applications)でbotを登録して入手することが出来ます。
また、`"message_room_id"`は以下のコマンドを実行することで入手することが出来ます。

```
python get_room_id.py
```

### 実行
```
python discordbot.py
```