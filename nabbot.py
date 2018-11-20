#!/usr/bin/env python3
import discord
from discord.ext import commands

import configparser
import json
from pprint import pprint
import random
from time import sleep
import re
from datetime import date
import asyncio
import sys
import select

from utils.dice import *
from utils.fortnite import *
from utils.responses import *
from utils.mtg import *

base_dir = "/home/ninhdo/discord/"
command_path = base_dir + "commands.json"

config = configparser.ConfigParser()
config.read(base_dir + "config.ini")

token = config["DEFAULT"]["token"]
bot = commands.Bot(command_prefix=config["DEFAULT"]["command_prefix"], description='Katie sucks', case_insensitive=True)

katie = 280428569174212610
zhong = 95480354386751488
ninh = 95468203374809088
nubbot = 473095940853727243

SHITPOST_CHANNEL = 347497327436759041
DEV_CHANNEL = 456556676288610307

TIMEOUT = 0.5
read_list = [sys.stdin]

@bot.event
async def on_ready():
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('--------')


@bot.event
async def on_message(message):
	sleep(0.3)
	if message.author == bot.user:
		return
	channel = message.channel
	# Attachment checks
	if message.author.id == nubbot:
#		for a in message.attachments:
#			print(a.filename)
		await cancel(message)
	# Check if the correct prefix is used
	if len(message.content) == 0:
		return
	if message.content[0] == config["DEFAULT"]["command_prefix"]:
		with open(command_path) as f:
			commands = json.load(f)
		command = message.content.split(" ", 1)[0][1:].lower()
		# Check if the command exists
		if command == "commands":
			await print_commands(channel)
		elif command in commands["Text"].keys():
			await channel.send(commands["Text"][command])
		elif command in commands["Katie"].keys():
			await channel.send(commands["Katie"][command]["text1"])
			sleep(commands["Katie"][command]["wait"])
			await channel.send(commands["Katie"][command]["text2"])
		elif command in commands["Dice"].keys():
			await roll_dice(message, channel)
		elif command in commands["Fortnite"]["Random"].keys():
			await fortnite_random_challenge(channel)
		elif command in commands["Fortnite"]["Print"].keys():
			await fortnite_print_challenges(channel)
		elif command in commands["Fortnite"]["Add"].keys():
			await fortnite_add_challenge(message, channel)
		elif command in commands["Fortnite"]["Delete"].keys():
			await fortnite_delete_challenge(message, channel)
		elif command in commands["Fortnite"]["Edit"].keys():
			await fortnite_edit_challenge(message, channel)
		elif command in commands["MTG"]["Print"].keys():
			await mtg_print_ids(channel)
		elif command in commands["MTG"]["Add"].keys():
			await mtg_add_id(message, channel)
		elif command in commands["MTG"]["Delete"].keys():
			await mtg_delete_id(message, channel)
		else:
			if message.content[1] == ".":
				return
			else:
				await channel.send("You did something wrong. Try `{}commands`".format(config["DEFAULT"]["command_prefix"]))
	if (bot.user.mentioned_in(message) and len(message.content.split(" ")) == 1):
		await i_am_here(channel)
	if message.content.lower() in json.load(open(bad_words_path)):
		await reverse(channel)
	if message.author.id == zhong or message.author.id == nubbot:
		await random_zhong_response(channel)
	if message.content.lower() in json.load(open(ikr_path)):
		await ikr(channel)
	if bot.user.mentioned_in(message) and "good" in message.content.lower().split(" "):
		await thanks(message, channel)
	if re.match("(.*)( - \w+ \d+)", message.content) and re.match("(.*)( - \w+ \d+)", message.content).span() == (0, len(message.content)):
		await lenny(message, channel)
	if len(message.mentions) >= 1 and message.mentions[0].id == katie and len(message.content.split(" ")) == 1:
		await fish(channel)
	if message.content == "testfish":
		await fish(channel)
	if bot.user.mentioned_in(message) and "play" in message.content.lower().split(" ") and "despacito" in message.content.lower().split(" "):
		await despacito(channel)

async def print_commands(channel):
	with open(command_path) as f:
		commands = json.load(f)
	return_message = ""
	return_message += "Dice:\n```md\n"
	for command in commands["Dice"].keys():
		return_message += "* {} \t {}\n".format(command, commands["Dice"][command])
	return_message += "```\n"
	return_message += "Fortnite Challenges:\n```md\n"
	for key in commands["Fortnite"].keys():
		for command in commands["Fortnite"][key].keys():
			return_message += "* {} \t {}\n".format(command, commands["Fortnite"][key][command])
	return_message += "```\n"
	return_message += "MTGA:\n```md\n"
	for key in commands["MTG"].keys():
		for command in commands["MTG"][key].keys():
			return_message += "* {} \t {}\n".format(command, commands["MTG"][key][command])
	return_message += "```"
	await channel.send(return_message)

async def say():
	await bot.wait_until_ready()
	channel = bot.get_channel(DEV_CHANNEL)
	if not channel:
		await asyncio.sleep(TIMEOUT)
	while not bot.is_closed():
		global read_list
		while read_list:
			ready = select.select(read_list, [], [], TIMEOUT)[0]
			if ready:
				for file in ready:
					line = file.readline()
					if not line:
						read_list.remove(line)
					elif line.rstrip():
						channel = None
						line = bytes(line, "utf-8").decode("utf-8", "ignore")
						try:
							if line.startswith("dev"):
								channel = bot.get_channel(DEV_CHANNEL)
								line = line[3:]
							else:
								channel = bot.get_channel(SHITPOST_CHANNEL)
							await channel.send(line)
						except:
							print("Error. Did not find the channel")
			else:
				await asyncio.sleep(TIMEOUT)
	await asyncio.sleep(TIMEOUT)
bot.loop.create_task(say())
bot.run(token)
