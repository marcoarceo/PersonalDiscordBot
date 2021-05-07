import discord
import os
from decouple import config

client = discord.Client()

client.run(config('TOKEN'))