import asyncio
import re
import random
from .responses import send_error

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
