import discord
import os
from decouple import config
from discord.ext import commands

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print("{0.user.name}".format(bot) + " has been activated")

@bot.command(name='hello')
async def SayHello(ctx):
    await ctx.send("Hello {}".format(ctx.message.author.mention))

bot.run(config('TOKEN'))