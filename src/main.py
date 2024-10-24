import os
import random
import logging
import subprocess
import discord
from discord.ext import commands

TOKEN = os.getenv('DISCORD_TOKEN')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger('discord_bot')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    # print(f'{bot.user} has connected to Discord!')
    logger.info(f'{bot.user} has connected to Discord!')

@bot.command(name='hello')
async def hello(ctx):
    await ctx.send(f"Wassup {ctx.author.name}!")

@bot.command(name='ping')
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command(name='roll')
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    logger.info(f"Roll command used by {ctx.author.name} [{ctx.author.status}] with {dice}")
    try:
        rolls, sides = map(int, dice.split('d'))
        logger.debug(f"Rolling {rolls} dice with {sides} sides")
    except Exception as e:
        logger.error(f"Invalid dice format: {dice}")
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, sides)) for r in range(rolls))
    logger.info(f"Roll result: {result}")
    await ctx.send(result)

@bot.command(name='inspire')
async def inspire(ctx):
    """Get an inspiring quote"""
    try:
        fortune_output = subprocess.check_output(
            "/usr/games/fortune | /usr/games/cowsay -f $(ls /usr/share/cowsay/cows/ | shuf -n1)",
            shell=True,
            text=True
        )

    except FileNotFoundError:
        fortune_output = "The 'fortune' command is not installed on this system."

    await ctx.send(fortune_output)


bot.run(TOKEN)
