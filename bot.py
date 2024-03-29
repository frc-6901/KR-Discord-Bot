# $ source bot-env/bin/activate

import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

# Bot Set Up
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

# Variables Set Up
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

# Actual Server
KNIGHTS_ROBOTICS_GUILD_ID = int(os.getenv('KNIGHTS_ROBOTICS_GUILD_ID'))
ANNOUNCEMENTS_CHANNEL_ID = int(os.getenv('ANNOUNCEMENTS_CHANNEL_ID'))
MENTOR_ROLE_ID = int(os.getenv('MENTOR_ROLE_ID'))

# Testing Server
TESTING_GUILD_ID = int(os.getenv('TESTING_GUILD_ID'))
TESTING_CHANNEL_ID = int(os.getenv('TESTING_CHANNEL_ID'))
TESTING_ROLE_ID = int(os.getenv('TESTING_ROLE_ID'))

TESTING = False


# When connected
@bot.event
async def on_ready():    
    print(f"{bot.user} is ONLINE in {[guild.name async for guild in bot.fetch_guilds()]}")


@bot.event
async def on_message(message):
    # If bot sent
    if message.author == bot.user:
        return

    # If not in #announcements
    if message.channel.id != TESTING_CHANNEL_ID if TESTING else ANNOUNCEMENTS_CHANNEL_ID:
        return

    # Get the server
    guild = bot.get_guild(TESTING_GUILD_ID if TESTING else KNIGHTS_ROBOTICS_GUILD_ID)
    
    # Each member in server
    async for member in guild.fetch_members():
        # If member is bot
        if member.bot:
            continue
        
        # If mentor
        if any(role.id == TESTING_ROLE_ID if TESTING else MENTOR_ROLE_ID for role in member.roles):
            continue
        
        # Send DM
        await member.send(message.content)


bot.run(BOT_TOKEN)