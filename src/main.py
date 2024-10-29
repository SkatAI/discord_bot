import os
import random
import logging
import subprocess
import discord
from discord import app_commands  # Add this import

from dotenv import load_dotenv
load_dotenv()


TOKEN = os.getenv('DISCORD_TOKEN')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger('discord_bot')

intents = discord.Intents.default()
intents.message_content = True

class MyBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        # Create a CommandTree instance
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # This is called when the bot starts
        await self.tree.sync()  # Sync commands with Discord

bot = MyBot()

@bot.event
async def on_ready():
    logger.info(f'{bot.user} has connected to Discord!')

@bot.tree.command(name="bonjour")
async def hello(interaction: discord.Interaction):
    """Says hello to the user"""
    await interaction.response.send_message(f"Salut {interaction.user.name}!")

@bot.tree.command(name="ping")
async def ping(interaction: discord.Interaction):
    """Responds with Pong!"""
    await interaction.response.send_message("Pong!")

@bot.tree.command(name="roll")
@app_commands.describe(dice="Format: NdN (e.g., 2d6 for rolling two six-sided dice)")
async def roll(interaction: discord.Interaction, dice: str):
    """Rolls a dice in NdN format."""
    logger.info(f"Roll command used by {interaction.user.name} with {dice}")
    try:
        rolls, sides = map(int, dice.split('d'))
        logger.debug(f"Rolling {rolls} dice with {sides} sides")
    except Exception as e:
        logger.error(f"Invalid dice format: {dice}")
        await interaction.response.send_message('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, sides)) for r in range(rolls))
    logger.info(f"Roll result: {result}")
    await interaction.response.send_message(result)

@bot.tree.command(name="inspire")
async def inspire(interaction: discord.Interaction):
    """Get an inspiring quote"""
    try:
        fortune_output = subprocess.check_output(
            "/usr/games/fortune | /usr/games/cowsay -f $(ls /usr/share/cowsay/cows/ | shuf -n1)",
            shell=True,
            text=True
        )
    except FileNotFoundError:
        fortune_output = "The 'fortune' command is not installed on this system."

    await interaction.response.send_message(fortune_output)

bot.run(TOKEN)