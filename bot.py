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
	
	if argv[0] == 'vote':
		m = await message.channel.send('Vote proposed by {0}: {1}'.format(message.author.mention, args))
		# await m.add_reaction("✅");
		# await m.add_reaction("✅");
	
	if content.startswith('info'):
		# Retrieves information about this guild.
		guild = message.guild
		e = discord.Embed(type='rich', color=discord.Colour.from_rgb(80, 160, 240))
		e.set_thumbnail(url=guild.icon_url)
		e.add_field(name='Name', value=guild.name)
		e.add_field(name='ID', value=guild.id)
		e.add_field(name='Created at', value=guild.created_at.strftime('%Y-%m-%d %H:%M:%S'))
		e.add_field(name='Owner', value=guild.owner)
		e.add_field(name='Members', value=guild.member_count)
		e.add_field(name='Channels', value=len(guild.channels))
		# e.add_field(name='Roles', value=len(guild.role_hierarchy)-1) # Remove @everyone
		e.add_field(name='Emoji', value=len(guild.emojis))
		e.add_field(name='Region', value=guild.region.name)
		e.add_field(name='Icon URL', value=guild.icon_url or 'This guild has no icon.')
		await message.channel.send(embed=e)
	
	if content.startswith('permissions'):
		w = { True: 'Yes', False: 'No' }
		
		# Store the channel
		channel = message.channel
		p = channel.permissions_for(message.author)
		e = discord.Embed(type='rich', color=discord.Colour.from_rgb(240, 160, 80))
		e.add_field(name='Read Messages', value=w[p.read_messages])
		e.add_field(name='Send Messages', value=w[p.send_messages])
		e.add_field(name='TTS', value=w[p.send_tts_messages])
		e.add_field(name='Manage Messages', value=w[p.manage_messages])
		e.add_field(name='Embed Links', value=w[p.embed_links])
		e.add_field(name='Attach Files', value=w[p.attach_files])
		e.add_field(name='Read Message History', value=w[p.read_message_history])
		e.add_field(name='Mention Everyone', value=w[p.mention_everyone])
		e.add_field(name='Change Nickanme', value=w[p.change_nickname])
		e.add_field(name='Manage Nicknames', value=w[p.manage_nicknames])
		e.add_field(name='Manage Roles', value=w[p.manage_roles])
		e.add_field(name='Manage Emoji', value=w[p.manage_emojis])
		e.add_field(name='Manage Channels', value=w[p.manage_channels])
		e.add_field(name='Kick Members', value=w[p.kick_members])
		e.add_field(name='Ban Members', value=w[p.ban_members])
		e.add_field(name='Administrator', value=w[p.administrator])
		await message.channel.send(embed=e)

# Run the discord bot
client.run(config['token'])