import discord
import os
import random
import youtube_dl

from decouple import config
from discord.ext import commands

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print("{0.user.name}".format(bot) + " has been activated")

@bot.command(name='hello')
async def SayHello(ctx):
    await ctx.send("Hello {}".format(ctx.message.author.mention))

@bot.command(name='play')
async def PlayMusic(ctx, url : str):
    # Check if there is already a song being played or stored
    currentSong = os.path.isfile("song.mp3")
    try:
        if currentSong:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    # Get the corresponding voice channel the message author is associated with
    voiceChannel = ctx.message.author.voice.channel
    if voiceChannel is None:
        await ctx.send("Please be in a voice channel when using this command")
        return
        
    # Connect the bot to the voice channel
    await voiceChannel.connect()
    # Get the bots voice client
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    # The youtube download settings that we need
    audioSettings = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    # Download the audio as an mp3
    with youtube_dl.YoutubeDL(audioSettings) as downloadedAudio:
        downloadedAudio.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")

    # Play the audio through the bot
    voice.play(discord.FFmpegPCMAudio("song.mp3"))

bot.run(config('TOKEN'))