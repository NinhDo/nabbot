import asyncio
import json
import re
from .responses import send_error

base_dir = "/home/ninhdo/discord/"
mtg_path = base_dir + "mtg.json"

mtg_regex = "[A-z-_0-9]+#\d{5}"

async def mtg_print_ids(channel):
	with open(mtg_path) as f:
		ids = json.load(f)
		response = "```md\nMTGA IDs\n"
		for i in ids:
			response += "{}: {}\n".format(i, ids[i])
		response += "```"
		await channel.send(response)

async def mtg_add_id(message, channel):
	if not message.author.top_role.permissions.administrator:
		await channel.send("Only a GOD can do this!")
		return
	hasName = False
	try:
		name = message.content.split(" ")[1]
		id = message.content.split(" ")[2]
		hasName = True
	except:
		try:
			id = message.content.split(" ")[1]
			hasName = False
		except:
			await channel.send("Yo, you're missing some info here. Either do addmtg [name] [id] or addmtg [id]")
			return
	if re.fullmatch(mtg_regex, id):
		with open(mtg_path, "r") as f:
			ids = json.load(f)
		with open(mtg_path, "w") as f:
			if hasName:
				ids[name] = id
			else:
				ids[message.author.display_name] = id
			json.dump(ids, f, indent=2)
			if hasName:
				await channel.send("Successfully added id for {}".format(name))
			else:
				await channel.send("Successfully added id for {}".format(message.author.mention))
	else:
		await channel.send("The ID is in the wrong format. Must be [Username]#[12345]. Just copy paste it from MTGA")

async def mtg_delete_id(message, channel):
	if not message.author.top_role.permissions.administrator:
		await channel.send("Only a GOD can do this!")
		return
	name = message.content.split(" ")[1]
	with open(mtg_path, "r") as f:
		ids = json.load(f)
	with open(mtg_path, "w") as f:
		exists = ids.pop("{}".format(name), False)
		json.dump(ids, f, indent=2)
		if exists:
			await channel.send("Deleted {} successfully".format(name))
		else:
			await channel.send("Unable to delete {}. Did you type the key correctly? It's CaSE SenSItiVe.".format(name))
