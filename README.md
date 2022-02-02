# discord bot (voice channel alert)
## function
ボイスチャンネルの入室時と退室時にアラートを行う．

入室時
```
<user>が<voice channel>に入室
```

退室時
```
<user>が<voice channel>を退室
```

## deploy
Herokuにデプロイする．

環境変数は以下の通りに設定する．
```
DISCORD_BOT_TOKEN=<Discord BotのToken>
DISCORD_MESSAGE_ROOM=<Discord Botがアラートを行うテキストチャンネルID>
```

## template
テンプレートとして以下を使用．圧倒的感謝．

https://github.com/DiscordBotPortalJP/discordpy-startup