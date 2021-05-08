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
    if ctx.message.author.voice:
        voiceChannel = ctx.message.author.voice.channel
    else:
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

@bot.command(name='pause')
async def PauseMusic(ctx):
    # Get the bots voice client
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    # Check to see if music is play, if yes, pause, if no, notify user
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("The bot is not playing any audio")

@bot.command(name='resume')
async def ResumeMusic(ctx):
    # Get the bots voice client
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    # Check to see if music is paused, if yes, resume, if no, notify user
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The bot audio is not paused")

@bot.command(name='stop')
async def StopMusic(ctx):
    # Get the bots voice client
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.stop()

@bot.command(name='leave')
async def LeaveVoice(ctx):
    # Get the bots voice client
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    # Check to see if the bot is connected, if yes, disconnect, if no, notify user
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not in a voice channel")

bot.run(config('TOKEN'))