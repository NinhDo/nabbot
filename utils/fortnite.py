import asyncio
import random
import json
import re
from .responses import send_error

base_dir = "/home/ninhdo/discord/"
challenges_path = base_dir + "challenges.json"

challenge_regex = "[A-z0-9\.\,\' \(\)]+"

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
	if re.fullmatch(challenge_regex, msg_content):
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
