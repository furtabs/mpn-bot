#***************************************************************************#
# Grotto Bot (Base)
#***************************************************************************#

import discord
import os
import json5

CONFIG_FILE = 'config.json5'

def load_config():
    if not os.path.exists(CONFIG_FILE):
        print(f"Warning: {CONFIG_FILE} not found. Please create it.")
        return {}
    with open(CONFIG_FILE, 'r') as f:
        return json5.load(f)

# Load config
config = load_config()
TOKEN = config.get('token')

# Set up intents
# message_content is REQUIRED for Leveling (giving XP on message) and Quotes (saving messages)
# members is REQUIRED for Birthdays (giving roles to members)
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Initialize the Bot
# Since you are using Pycord and slash commands, discord.Bot is the best choice
bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print('*************************************************')
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print(f'Connected to {len(bot.guilds)} servers.')
    print('*************************************************')

# Load Cogs
if __name__ == '__main__':
    # Ensure the cogs directory exists
    if not os.path.exists('./cogs'):
        os.makedirs('./cogs')
        print("Created 'cogs' folder. Please move your python feature files there.")

    # Loop through the cogs folder and load all python files
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and not filename.startswith('_'):
            cog_name = f'cogs.{filename[:-3]}'
            try:
                bot.load_extension(cog_name)
                print(f'✅ Successfully loaded extension: {filename}')
            except Exception as e:
                print(f'❌ Failed to load extension {filename}: {e}')

    # Run the bot
    if TOKEN:
        print("Starting bot...")
        bot.run(TOKEN)
    else:
        print("❌ Error: No bot token found in config.json5! Please add your 'token'.")
