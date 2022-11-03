# discord bot (voice channel alert)
## function
### 入退室通知
ユーザがボイスチャンネルに入退室を行った場合に、環境変数に指定したテキストチャンネルで通知を行います。

入室時
```
<user>が<voice channel>に入室
```

退室時
```
<user>が<voice channel>を退室
```

### 作業時間通知
毎週月曜日の21:00に誰が何時間ボイスチャンネルに入室していたかを表示します。
```
今週の作業時間
Taro : 5H31M
Hanako : 3H0M
...
```

## deploy
Herokuにデプロイする。

環境変数は以下の通りに設定する。
```
DISCORD_BOT_TOKEN=<Discord BotのToken>
DISCORD_MESSAGE_ROOM=<Discord Botがアラートを行うテキストチャンネルID>
```

## template
テンプレートとして以下を使用。
https://github.com/DiscordBotPortalJP/discordpy-startup