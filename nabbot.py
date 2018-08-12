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

base_dir = "/home/ninhdo/discord/"
command_path = base_dir + "commands.json"
challenges_path = base_dir + "challenges.json"
img_path = base_dir + "img/"
bad_words_path = base_dir + "bad_words.json"
zhong_response_images = [
	"AreYouKiddingMe.png", 
	"ThatsAllWrong.png", 
	"IsThatSo.png", 
	"Horror.png", 
	"IDoubtIt.png", 
	"NoThanks.png", 
	"saitama.png", 
	"WhatAPerfectWayToPutIt.png", 
	"kacchan.png",
	"Tatsumaki.png"
]
fish_gif = "fish.mp4"
ikr_path = base_dir + "ikr.json"

config = configparser.ConfigParser()
config.read("/home/ninhdo/discord/config.ini")

token = config["DEFAULT"]["token"]
bot = commands.Bot(command_prefix=config["DEFAULT"]["command_prefix"], description='Katie sucks', case_insensitive=True)
challenge_regex = "[A-z0-9\.\,\' \(\)]+"

RESPONSE_CHANCE = 5

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
	if bot.user.mentioned_in(message) and "play" in message.content.lower().split(" ") and "despacito" in message.content.lower().split(" "):
		await despacito(channel)

async def print_commands(channel):
	with open(command_path) as f:
		commands = json.load(f)
	return_message = ""
	return_message += "Dice:\n ```md\n"
	for command in commands["Dice"].keys():
		return_message += "* {} \t {}\n".format(command, commands["Dice"][command])
	return_message += "```\n"
	return_message += "Fortnite Challenges:\n```md\n"
	for key in commands["Fortnite"].keys():
		for command in commands["Fortnite"][key].keys():
			return_message += "* {} \t {}\n".format(command, commands["Fortnite"][key][command])
	return_message += "```"
	await channel.send(return_message)

async def roll_dice(message, channel):
	roll_text = message.content.split(" ", 1)[1].lower()
	if re.match("[^d0-9\(\)+\-*/]+", roll_text):
		await send_error(channel)
		return
	# Split into multiple rolls
	rolls = re.split("(\d+d\d+|d\d+|\d+)", roll_text)
	# Remove whitespace
	rolls[:] = [r.strip() for r in rolls if r]
	# Check if all parts are valid
	for roll in rolls:
		# Must be xdy, dy, y, +, -, *, /, ( or )
		if not re.match("\d+d\d+|d\d+|\d+|[+\-*/\(\)]+", roll):
			await send_error(channel)
			return
	# Make rolls into numbers
	rolls[:] = ["1{}".format(r) if re.match("d\d+", r) else r for r in rolls]
	rolls[:] = ["`{}`".format(int(r.split("d")[0]) * random.randint(1, int(r.split("d")[1]))) if re.match("\d+d\d+", r) else r for r in rolls]
	final_string = "".join(rolls[:])
	final_zero = False
	if re.match(".*[+\-]$", final_string):
		final_string = final_string + "0"
		final_zero = True
	eval_string = re.sub("`", "", final_string)
	try:
		result = eval(eval_string)
		if final_zero:
			final_string = final_string[:-1]
		await channel.send("`{}` = {} = {}".format(roll_text, final_string, result))
	except:
		await send_error(channel)


async def fortnite_random_challenge(channel):
	with open(challenges_path) as f:
		challenges = json.load(f)
		random_challenge = random.choice(challenges)
		await channel.send(random_challenge)

async def fortnite_print_challenges(channel):
	with open(challenges_path) as f:
		challenges = json.load(f)
		response = "```md\nAll Fortnite Challenges\n"
		for i, challenge in enumerate(challenges):
		        response += "{}. {}\n".format(i, challenge)
		response += "```"
		await channel.send(response)

async def fortnite_add_challenge(message, channel):
	if not message.author.top_role.permissions.administrator:
		await channel.send("Only a GOD can do this!")
		return
	msg_content = message.content.split(" ", 1)[1]
	if re.match(challenge_regex, msg_content).span() == (0, len(msg_content)):
		with open(challenges_path, "r") as f:
			challenges = json.load(f)
		with open(challenges_path, "w") as f:
			challenges.append(msg_content)
			json.dump(challenges, f, indent=2)
			await channel.send("Fortnite Challenge `{}` added successfully".format(msg_content))
	else:
		await send_error(channel)


async def fortnite_delete_challenge(message, channel):
	if not message.author.top_role.permissions.administrator:
		await channel.send("Only a GOD can do this!")
		return
	msg_content = message.content.split(" ", 1)[1]
	if re.match("\d+", msg_content).span() == (0, len(msg_content)):
		with open(challenges_path, "r") as f:
			challenges = json.load(f)
		try:
			with open(challenges_path, "w") as f:
				del challenges[int(msg_content)]
				json.dump(challenges, f, indent=2)
				await channel.send("Fortnite Challenge #{} deleted successfully".format(msg_content))
		except:
			await channel.send("Unable to delete Fortnite Challenge #{}".format(msg_content))
	else:
		await send_error(channel)

async def fortnite_edit_challenge(message, channel):
	if not message.author.top_role.permissions.administrator:
		await channel.send("Only a GOD can do this!")
		return
	try:
		index = int(message.content.split(" ", 2)[1])
		msg_content = message.content.split(" ", 2)[2]
	except:
		await channel.send("Message must be in the form [Challenge Number] [New Challenge]")
	if re.match(challenge_regex, msg_content).span() == (0, len(msg_content)):
		with open(challenges_path, "r") as f:
			challenges = json.load(f)
		try:
			with open(challenges_path, "w") as f:
				challenges[index] = msg_content
				json.dump(challenges, f, indent=2)
				await channel.send("Fortnite Challenge #{} changed to `{}`.".format(index, msg_content))
		except:
			await channel.send("Unable to edit Fortnite Challenge #{}.".format(index))
	else:
		await send_error(channel)

async def reverse(channel):
	if random.randint(1, 100) <= 50:
		return
	with open(img_path + "reverse.png", "rb") as f:
		await channel.send(file=discord.File(f, "reverse.png"))

async def random_zhong_response(channel):
	if random.randint(1, 100) <= RESPONSE_CHANCE:
		with open(img_path + random.choice(zhong_response_images), "rb") as f:
			await channel.send(file=discord.File(f, "response.png"))

async def ikr(channel):
	await channel.send("ikr")

async def i_am_here(channel):
	await channel.send("Mo daijoubu! Naze tte? Watashi ga kita!")

async def send_error(channel):
	await channel.send(config["DEFAULT"]["error_msg"])

async def lenny(message, channel):
#	if re.match("(.*)( - \w+ \d+)", message.content).span() == (0, len(message.content)):
	if channel.id == 452998105407815691 or channel.id == 456556676288610307:
		await channel.send("\u0028 \u0361\u00b0 \u035c\u0296 \u0361\u00b0\u0029")

async def wednesday():
	flag = False
	await bot.wait_until_ready()
	channel = bot.get_channel(347497327436759041)
	if not channel:
		print("Yo, somethings wrong with wednesday")
		await asyncio.sleep(TIMEOUT)
	while not bot.is_closed():
		if date.today().weekday() == 2 and date.today().hour == 12 and not flag: # If wednesday
			await channel.send("It's Wednesday My Dudes")
			flag = True
		else:
			if flag and not date.today().hour == 12:
				flag = False
		await asyncio.sleep(TIMEOUT)

async def thanks(message, channel):
	await channel.send("Thanks, {}! :D".format(message.author.mention))

async def angry(message, channel):
	await channel.send(">:C {}".format(message.author.mention))

async def fish(channel):
	with open(img_path + fish_gif, "rb") as f:
		await channel.send(file=discord.File(f, "reeling_in_katie.mp4"))

async def despacito(channel):
	await channel.send("Now playing: `Despacito 2 (ft. Lil' Pump)`\n\n ------------:small_orange_diamond:------------------\n\n◄◄▐▐ ►►   1:17 / 4:20   ------:small_blue_diamond: :loud_sound:")

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
#bot.loop.create_task(wednesday())
bot.loop.create_task(say())
bot.run(token)

