import discord
import logging
import yaml

try:
	from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
	from yaml import Loader, Dumper

from cliparser import parsecommand

# Config
config = yaml.load(open('config.yml', 'r'), Loader=Loader)
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
		return  # Ignores messages of myself
	
	if message.tts:
		await message.channel.send('/!\ Warning: Use of TTS by {0}.'.format(message.author.mention))
	if message.mention_everyone:
		await message.channel.send('/!\ Warning: {0} mentioned everyone.'.format(message.author.mention))

	content = message.content
	if content.startswith(PREFIX):
		content = content[len(PREFIX):]
	else:
		return  # Not a command.
	
	argc, argv, args = parsecommand(content)
	
	if content.startswith('hello'):
		await message.channel.send('Hello, {0}!'.format(message.author.mention))
	
	if content.startswith('parse'):
		await message.channel.send('Get parsed! {0}'.format(args))

# Run the discord bot
client.run(config['token'])