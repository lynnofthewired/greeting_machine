import discord
import os
import json
import asyncio
from discord.ext import commands
from discord import PermissionOverwrite, Permissions

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True
intents.members = True

with open('config.json') as config_file:
    config = json.load(config_file)

CARELESSLOVE_ID = config['carelesslove_id']
BGR_WELCOME = config['bgr_welcome']
CL_CHATTER = config['cl_chatter']
CL_PRIVATE = config['cl_private']

bot = commands.Bot(command_prefix='$', intents=intents)

pronoun_roles = []
guild = None

async def update_pronoun_roles():
    global pronoun_roles
    global guild
    while True:
        if guild is not None:
            pronoun_roles = [role for role in guild.roles if '/' in role.name]
        await asyncio.sleep(7200)  # wait for 2 hours

def role_numbers_check(message):
    return all(i.isdigit() and 0 < int(i) <= len(pronoun_roles) for i in message.content.split(' '))

@bot.command()
async def intro(ctx):
    await ctx.send(f"hello, {ctx.guild.name}. i am the greeting machine. i will greet users when they join this server.\n\ni will also help users add or remove pronoun roles. to do this, begin by typing \"``$pronouns``\"\n\n**see below for a full list of greeting machine commands**:\n\n``$intro`` - repeats this introduction\n``$pronouns`` - prints a full list of this server's roles that are associated with preferred pronouns\n``$assign`` - if you already know the number associated with your preferred pronoun as it is printed with the \"``$pronouns``\" command, you can use \"``$assign``\" instead. this skips the step of printing the list, and can look like \"``$assign 1``\", or \"``$assign 1 and 2``\", or \"``$assign 1 2 & 3``\", and so on.\n\nif you do not see your preferred pronouns in our listing, please either tag or direct message the administrator.")

@bot.command()
async def pronouns(ctx):
    global pronoun_roles
    global guild
    guild = ctx.guild
    response = "\n".join(f"{i+1}. {role.name}" for i, role in enumerate(pronoun_roles))
    await ctx.send("\nplease reply with the number(s) corresponding to your preferred pronouns:\n" + response + "\n\nif you do not see your preferred pronouns in our listing, please tag the administrator right here.")
    
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        message = await bot.wait_for('message', check=check, timeout=60.0)
        numbers = []
        parts = message.content.split()
        for part in parts:
            if part.isdigit():
                number = int(part)
                if 0 < number <= len(pronoun_roles):
                    numbers.append(number)
        for number in numbers:
            role_to_toggle = pronoun_roles[number-1]
            if role_to_toggle in ctx.author.roles:
                await ctx.author.remove_roles(role_to_toggle)
                action = "removed"
            else:
                await ctx.author.add_roles(role_to_toggle)
                action = "added"
            await ctx.send(f"the role {role_to_toggle.name} has been {action}.")
    except asyncio.TimeoutError:
        await ctx.send('you took too long to respond. try sending "``$pronouns``" again.')
        return

@bot.command()
async def assign(ctx, *args):
    global pronoun_roles
    numbers = []
    for arg in args:
        try:
            number = int(arg)
            if 0 < number <= len(pronoun_roles):
                numbers.append(number)
        except ValueError:
            continue  
    for number in numbers:
        role_to_toggle = pronoun_roles[number-1]
        if role_to_toggle in ctx.author.roles:
            await ctx.author.remove_roles(role_to_toggle)
            action = "removed"
        else:
            await ctx.author.add_roles(role_to_toggle)
            action = "added"
        await ctx.send(f"the role {role_to_toggle.name} has been {action}.")

@bot.event
async def on_ready():
    global guild
    print('We have logged in as {0.user}'.format(bot))
    guild = bot.guilds[0]  # assuming the bot is only in one guild
    bot.loop.create_task(update_pronoun_roles())

@bot.event
async def on_member_join(member):
    if member.guild.id == CARELESSLOVE_ID:
        channel = bot.get_channel(CL_PRIVATE) 
        if channel:
            await channel.send(f'welcome to {member.guild.name}, {member.mention}.\na black wind howls. join our futile prattle as we try to fill the void.\n\nif you wish, please tell us which pronouns we should use for you, which you can begin by typing "``$pronouns``"')
    else:
        channel = bot.get_channel(BGR_WELCOME)
        if channel:
            await channel.send(f':bubbles::sparkles:welcome to {member.guild.name}, {member.mention}:sparkles::bubbles:\n\nplease carefully read the #rules channel, and follow its instructions\n\nnext, please feel free to introduce yourself, and tell us which pronouns we should use for you, which you can begin by typing "``$pronouns``"')

bot.run(config['token'])



# replace this channel ID before launching to Big Gay Roc: 916374828112576533
# also maybe attach this text or something like it: "To tell me your preferred pronouns, begin by posting "/pronouns" and I will prompt you from there!"


# bot's invite link with desired scopes and permissions:
# https://discord.com/api/oauth2/authorize?client_id=703424325251891300&permissions=2416430144&scope=bot