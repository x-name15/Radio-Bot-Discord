import os
import asyncio
import discord
from discord import FFmpegPCMAudio
from discord import Embed
from discord.ext.commands import Bot

token = ""
prefix = "$"

streams = [
    {"name": "Radiorecord.ru", "link": "https://air.radiorecord.ru:805/synth_320"},
    {"name": "Nightride.fm", "link": "https://stream.nightride.fm/nightride.m4a"},
    {"name": "Synthwave.hu", "link": "https://ecast.myautodj.com/public1channel"},
    {"name": "Laut.fm", "link": "https://nightdrive.stream.laut.fm/nightdrive"},
    {"name": "I love Radio", "link": "https://streams.ilovemusic.de/iloveradio10.mp3"},
    {"name": "MonsterCat Radio", "link": "https://streams.ilovemusic.de/iloveradio24.mp3"},
    {"name": "Chill and Lofi House", "link": "https://streams.ilovemusic.de/iloveradio17.mp3"},
    {"name": "MainStage Madness", "link": "https://streams.ilovemusic.de/iloveradio22.mp3"},
    {"name": "Mashup Radio", "link": "https://streams.ilovemusic.de/iloveradio5.mp3"},
    {"name": "The Hard Club", "link": "https://streams.ilovemusic.de/iloveradio20.mp3"},
    {"name": "The Floor Radio", "link": "https://streams.ilovemusic.de/iloveradio14.mp3"},
    {"name": "New Pop", "link": "https://streams.ilovemusic.de/iloveradio11.mp3"},
    {"name": "The Sun and Beach", "link": "https://streams.ilovemusic.de/iloveradio15.mp3"},
    {"name": "X-Mas", "link": "https://streams.ilovemusic.de/iloveradio8.mp3"}

]

bot = Bot(command_prefix = prefix)
bot.remove_command('help')

@bot.event
async def on_ready():
    print("The bot is online!")
    print("------------------------------")
    print(f"Logued in: {bot.user.name}")
    print(f'ID of the Bot: {bot.user.id}')
    print("-------------------------------")

@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! `{round(bot.latency * 1000)} ms`")

async def play_stream(ctx, msg):
    """ Plays a stream link"""
    if ctx.voice_client is None:
        global player
        channel = ctx.message.author.voice.channel
        player = await channel.connect()
    if player.is_playing():
        player.stop()
    player.play(
        FFmpegPCMAudio(
            streams[(int(msg.content) - 1) if type(msg) != int else (msg - 1)]["link"]
        )
    )
    await ctx.send(
        f"Playing the Radio - **`{streams[(int(msg.content) -1) if type(msg) != int else (msg - 1)]['name']}`**"
    )

@bot.command()
async def rplay(ctx, channel: int = 0):
    if not ctx.message.author.voice:
        await ctx.send("Connect to a Voice Channel to start the radio")
        return  
    if channel > 4: 
        return
    if channel != 0:
        await play_stream(ctx, channel)
        return
    radio_channel_prompt = f"""
    `📻 | Radio Discord`
   Select a radio channel -
> 1. **`Radiorecord.ru`**
> 2. **`Nightride.fm`**
> 3. **`Synthwave.hu`**
> 4. **`Laut.fm`**
> 5. **`IloveRadio`**
> 6. **`MonsterCat Radio`**
> 7. **`Chill and Lofi House`**
> 8. **`MainStage Madness`**
> 9. **`Mashup Radio`**
> 10. **`The Hard Club`**
> 11. **`The Floor Radio`**
> 12. **`New Pop`**
> 13. **`The Sun and Beach`**
> 14. **`X-Mas`**
    """
    await ctx.send(radio_channel_prompt)
    def check(msg):
        return (
            msg.author == ctx.author
            and msg.channel == ctx.channel
            and msg.content.isnumeric()
            and int(msg.content) in [i + 1 for i in range(len(streams))]
        )
    msg = 0
    try:
        msg = await bot.wait_for("message", check=check, timeout=20)
    except asyncio.TimeoutError:
        await ctx.send("Sorry you didn't answer in time :C")
        return
    try:
        await play_stream(ctx, msg)
    except Exception as e:
        print(f"[ERROR]: {e}")

@bot.command()
async def rstop(ctx):
    if ctx.voice_client is None:
        await ctx.send("I'm not playing a radio right now !!!1!1!")
        return
    else:
        player.stop()
        await ctx.send("Radio disconnected and paused correctly")
        await ctx.guild.voice_client.disconnect(force=True)

@bot.command()
async def help(ctx):
  imageURL = "https://i.imgur.com/w5XnsL3.png"
  embed=discord.Embed(title="Help Command", description="Hey im a Radio for Discord", color=0x3194bf)
  embed.set_author(name="Help", url="https://github.com/x-name15/Radio-Bot-Discord", icon_url="https://i.imgur.com/w5XnsL3.png")
  embed.set_image(url=imageURL)
  embed.add_field(name="rplay", value="Starts the Radio in a Voice Channel", inline=False)
  embed.add_field(name="rstop", value="Stop and Disconnect the Radio from Voice Channel", inline=False)
  embed.set_footer(text="This bot is open-source: https://github.com/x-name15/Radio-Bot-Discord")
  await ctx.send(embed=embed)
bot.run(token)
