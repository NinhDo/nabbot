import asyncio
import json
import re
from .responses import send_error

base_dir = "/home/ninhdo/discord/"
nfc_path = base_dir + "nintendo.json"

nfc_regex = "\d{4}-\d{4}-\d{4}"

async def nfc_print_fcs(channel):
	with open(nfc_path) as f:
		fcs = json.load(f)
		response = "```md\nNintendo Friend Codes\n"
		for i in fcs:
			response += "{}: {}\n".format(i, fcs[i])
		response += "```"
		await channel.send(response)

async def nfc_add_fc(message, channel):
	hasName = False
	try:
		name = message.content.split(" ")[1]
		fc = message.content.split(" ")[2]
		hasName = True
	except:
		try:
			fc = message.content.split(" ")[1]
			hasName = False
		except:
			await channel.send("Yo, you're missing some info here. Either do addnfc [name] [fc] or anfc [fc]")
			return
	if re.fullmatch(nfc_regex, fc):
		with open(nfc_path, "r") as f:
			fcs = json.load(f)
		with open(nfc_path, "w") as f:
			if hasName:
				fcs[name] = fc
			else:
				fcs[message.author.display_name] = fc
			json.dump(fcs, f, indent=2)
			if hasName:
				await channel.send("Successfully added FC for {}".format(name))
			else:
				await channel.send("Successfully added FC for {}".format(message.author.mention))
	else:
		await channel.send("The FC is in the wrong format. Must be 1234-1234-1234.")

async def nfc_delete_fc(message, channel):
	if not message.author.top_role.permissions.administrator:
		await channel.send("Only a GOD can do this!")
		return
	name = message.content.split(" ")[1]
	with open(nfc_path, "r") as f:
		fcs = json.load(f)
	with open(nfc_path, "w") as f:
		exists = fcs.pop("{}".format(name), False)
		json.dump(fcs, f, indent=2)
		if exists:
			await channel.send("Deleted {} successfully".format(name))
		else:
			await channel.send("Unable to delete {}.".format(name))
