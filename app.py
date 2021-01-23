from vk_connect import login, get_info, send_command

def main():
	vk = login()
	data = get_info(vk)

	if data["can_feed"] == 1:
		send_command(vk, "feed")

	if data["on_work"] == 0:
		send_command(vk, "work")
	elif data["on_work"] == 1:
		send_command(vk, "end_work")

	if data["status"] == "Нуждается в реанимации":
		if data["heal"] > 0:
			send_command(vk, "use_heal")
		elif data["money"] >= 300:
			send_command(vk, "buy_heal")
			send_command(vk, "use_heal")

	if data["feel"] == "Плохое":
		if data["lollipop"] > 0:
			send_command(vk, "use_lp")
		elif data["money"] >= 300:
			send_command(vk, "buy_lp")
			send_command(vk, "use_lp")


if __name__=='__main__':
	main()