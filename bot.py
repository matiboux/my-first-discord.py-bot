import yaml
import discord
import logging

# Config
config = yaml.load(open('config.yml', 'r'))
PREFIX = config['prefix']

# Logging
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Discord bot
client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(PREFIX + 'hello'):
        await message.channel.send('Hello, {0}!'.format(message.author.mention))

client.run(config['token'])