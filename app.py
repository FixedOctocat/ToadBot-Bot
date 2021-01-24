from json import load, dump
from time import time, sleep
from vk_connect import login, get_info, send_command

def main():
	with open('JabkaData.json', 'r', encoding='utf-8') as f:
		data = load(f)

	while True:
		time_ = time()

		if data["can_feed"] == 1:
			print("Кормим жабку")
			send_command(vk, "feed")
			data["can_feed"] = 0
			data["feed_time"] = time_ + 12*60*60

		if data["on_work"] == 0:
			if data["work_time"] < time_:
				print("Отправили жабку на работу")
				send_command(vk, "work")
				data["work_time"] = time_ + 2*60*60
		elif data["on_work"] == 1:
			if data["work_time"] < time_:
				print("Забрали жабку с работы")
				send_command(vk, "end_work")
				data["work_time"] = time_ + 6*60*60
				data = get_info(vk)

		if data["status"] == "Нуждается в реанимации":
			if data["heal"] > 0:
				send_command(vk, "use_heal")
				data["heal"] -= 1
			elif data["money"] >= 300:
				send_command(vk, "buy_heal")
				data["money"] -= 300
				print("Купили аптечку")
				send_command(vk, "use_heal")
			
			print("Вылечили жабку")
			data["status"] = "Живая"

		if data["feel"] == "Плохое":
			if data["lollipop"] > 0:
				send_command(vk, "use_lp")
				data["lollipop"] -= 1
			elif data["money"] >= 300:
				send_command(vk, "buy_lp")
				data["money"] -= 300
				print("Купили леденец")
				send_command(vk, "use_lp")

			print("Задобрили жабку")
			data["feel"] = "Нормальное"

		with open('JabkaData.json', 'w', encoding='utf-8') as f:
			dump(data, f, ensure_ascii=False, indent=4, sort_keys=True)
		
		sleep(min(data["feed_time"], data["work_time"]))

if __name__=='__main__':
	vk = login()

	choice = input("Обновить данные о жабке? [Y/n] ")
	if choice.lower() == "y":
		data = get_info(vk)
		print("Все узнали")

	main()