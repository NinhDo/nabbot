import asyncio
import random
import json
import discord

base_dir = "/home/ninhdo/discord/"
img_path = base_dir + "img/"
bad_words_path = base_dir + "bad_words.json"
zhong_response_images = [
	"AH.png",
	"AreYouKiddingMe.png",
	"ThatsAllWrong.png",
	"IsThatSo.png",
	"Horror.png",
	"IDoubtIt.png",
	"NoThanks.png",
	"saitama.png",
	"WhatAPerfectWayToPutIt.png",
	"kacchan.png",
	"Tatsumaki.png",
	"kaminari.png",
	"laius.png",
	"midoriya.png"
]
fish_gif = "fish.gif"
ikr_path = base_dir + "ikr.json"

RESPONSE_CHANCE = 5

async def reverse(channel):
	if random.randint(1, 100) <= 50:
		return
	with open(img_path + "reverse.png", "rb") as f:
		await channel.send(file=discord.File(f, "reverse.png"))

async def cancel(message):
	for a in message.attachments:
		if a.filename == "skip-card.png":
			if random.randint(1, 100) <= 50:
				return
			with open(img_path + "spellpierce.jpg", "rb") as f:
				await message.channel.send(file=discord.File(f, "spellpierce.jpg"))
			return

async def random_zhong_response(channel):
	if random.randint(1, 100) <= RESPONSE_CHANCE:
		with open(img_path + random.choice(zhong_response_images), "rb") as f:
			await channel.send(file=discord.File(f, "response.png"))

async def ikr(channel):
	await channel.send("ikr")

async def i_am_here(channel):
	await channel.send("Mo daijoubu! Naze tte? Watashi ga kita!")

async def lenny(message, channel):
#	if re.match("(.*)( - \w+ \d+)", message.content).span() == (0, len(message.content)):
	if channel.id == 452998105407815691 or channel.id == 456556676288610307:
		await channel.send("\u0028 \u0361\u00b0 \u035c\u0296 \u0361\u00b0\u0029")

async def thanks(message, channel):
	await channel.send("Thanks, {}! :D".format(message.author.mention))

async def angry(message, channel):
	await channel.send(">:C {}".format(message.author.mention))

async def fish(channel):
	with open(img_path + fish_gif, "rb") as f:
		await channel.send(file=discord.File(f, "reeling_in_katie.gif"))

async def despacito(channel):
	await channel.send("Now playing: `Despacito 2 (ft. Lil' Pump)`\n\n ------------:small_orange_diamond:------------------\n\n◄◄▐▐ ►►   1:17 / 4:20   ------:small_blue_diamond: :loud_sound:")

async def send_error(channel):
	await channel.send("That doesn't look like anything to me.")
