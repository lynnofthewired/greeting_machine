import discord
import os
import json
import io
from discord.ext import commands
from discord import PermissionOverwrite, Permissions

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True
intents,members = True # Enables member join/leave events

bot = commands.Bot(command_prefix='$', intents=intents) # the command prefix can be anything. if we have a command called ping', you would call it with '$ping'. "intents" is a variable in which we have passed all the above listed intents.

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot)) # format is a Python method for formatting a string, and the argument "bot" says that the context for the curly bracket content is the variable, "bot"

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(916374828112576533) # The channel ID
    if channel:
        await channel.send(f'Hello new user! To tell me your preferred pronouns, begin by posting "/pronouns" and I will prompt you from there!')

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f'An error occurred: {str(error)}')

with open('config.json') as config_file:
    config = json.load(config_file)

bot.run(config['token'])