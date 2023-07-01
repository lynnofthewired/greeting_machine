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
intents.members = True # Enables member join/leave events

bot = commands.Bot(command_prefix='$', intents=intents) # the command prefix can be anything. if we have a command called ping', you would call it with '$ping'. "intents" is a variable in which we have passed all the above listed intents.

@bot.command()
async def pronouns(ctx):
    pronoun_roles = [role for role in ctx.guild.roles if '/' in role.name]
    response = "\n".join(f"{i+1}. {role.name}" for i, role in enumerate(pronoun_roles))
    await ctx.send("Please reply with the number corresponding to your pronouns:\n" + response)

@bot.command()
async def choose(ctx, number: int):
    pronoun_roles = [role for role in ctx.guild.roles if '/' in role.name]
    role_to_add = pronoun_roles[number-1]  # Subtract 1 because list indices start at 0
    await ctx.author.add_roles(role_to_add)
    await ctx.send(f"You have been assigned the role: {role_to_add.name}")

@bot.command()
async def remove_role(ctx, Member: discord.Member, *, role_name):
    if role:
        try:
            await member.remove_roles(role)
            await ctx.send(f"The role {role_name} has been removed from {member.display_name}")

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot)) # format is a Python method for formatting a string, and the argument "bot" says that the context for the curly bracket content is the variable, "bot"

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(337380248457052161) # The channel ID
    if channel:
        await channel.send(f'Hello, {member.mention}!')

# @bot.event
#async def on_command_error(ctx, error):
    #await ctx.send(f'An error occurred: {str(error)}')

with open('config.json') as config_file:
    config = json.load(config_file)

bot.run(config['token'])

# replace this channel ID before launching to Big Gay Roc: 916374828112576533
# also maybe attach this text or something like it: "To tell me your preferred pronouns, begin by posting "/pronouns" and I will prompt you from there!"