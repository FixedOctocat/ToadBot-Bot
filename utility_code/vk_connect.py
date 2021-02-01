# -*- coding: utf-8 -*-
import vk_api
from json import load, dump
from time import time, sleep
from conf import access_token, chat_id
from vk_api.utils import get_random_id

commands = {
	"perks": "Моя жаба",
	"info": "Жаба инфо",
	"feed": "Покормить жабу",
	"mega_feed": "Откормить жабу",
	"invent": "Мой инвентарь",
	"heal": "Реанимировать жабу",
	"work": "Отправить жабу на работу",
	"end_work": "Завершить работу",
	"buy_lp": "Приобрести леденцы 1",
	"use_lp": "Использовать леденцы",
	"buy_heal": "Приобрести аптечку",
	"use_heal": "Реанимировать жабу",
}

def login():
	try:
		"""login via token"""
		vk_session = vk_api.VkApi(token=access_token)
		vk = vk_session.get_api()
		vk.messages.getConversations(peer_id=2000000000+chat_id, count=1, random_id=get_random_id())
		return vk
	except vk_api.exceptions.ApiError:
		return None
	except:
		return 1

def get_info(vk):
	try:
		"""open and save data"""
		try:
			with open('JabkaData.json', 'r', encoding='utf-8') as f:
				data = load(f)
		except FileNotFoundError:
			data = {}

		"""send perks command"""
		vk.messages.send(chat_id=chat_id, message=commands["perks"], random_id=get_random_id())
		sleep(1)
		info = vk.messages.getConversations(peer_id=2000000000+chat_id, count=1, random_id=get_random_id())["items"][0]["last_message"]["text"].split("\n")
		vk.messages.markAsRead(peer_id=2000000000+chat_id, mark_conversation_as_read=1, random_id=get_random_id())

		data["xp"] = int(info[2][info[2].find(":")+2:info[2].find("/"):])
		data["feel"] = info[7][info[7].find(":")+2::]
		data["level"] = int(info[1][info[1].find(":")+2::])
		data["money"] = int(info[5][info[5].find(":")+2::])
		data["status"] = info[4][info[4].find(":")+4::]

		"""send info command"""
		vk.messages.send(chat_id=chat_id, message=commands["info"], random_id=get_random_id())
		sleep(1)
		info = vk.messages.getConversations(peer_id=2000000000+chat_id, count=1, random_id=get_random_id())["items"][0]["last_message"]["text"].split("\n")
		vk.messages.markAsRead(peer_id=2000000000+chat_id, mark_conversation_as_read=1, random_id=get_random_id())
		
		if "Можно покормить через" in info[0]:
			data["can_feed"] = 0
			ft = info[0].split(" ")[-1].replace("ч", "").replace("м", "").split(":")
			data["feed_time"] = time() + int(ft[0])*60*60 + int(ft[1])*60
		elif "Жабу можно покормить" in info[0]:
			data["can_feed"] = 1
		
		if "можно отправить на работу" in info[2]:
			data["on_work"] = 0
			data["work_time"] = 0
		elif "Можно забрать жабу с работы" in info[2]:
			data["on_work"] = 1
			data["work_time"] = 0
		elif "Забрать жабу можно" in info[2]:
			data["on_work"] = 1
			wt = info[0].split(" ")[-1].replace("ч", "").replace("м", "").split(":")
			data["work_time"] = time() + int(wt[0])*60*60 + int(wt[1])*60
		elif "Отправить на работу можно" in info[2]:
			data["on_work"] = 0
			wt = info[0].split(" ")[-1].replace("ч", "").replace("м", "").split(":")
			data["work_time"] = time() + int(wt[0])*60*60 + int(wt[1])*60

		if "Можно откормить" in info[1]:
			data["mega_feed"] = 1
		elif "Откормить через" in info[1]:
			data["mega_feed"] = 0
		
		"""get inventory"""
		vk.messages.send(chat_id=chat_id, message=commands["invent"], random_id=get_random_id())
		sleep(1)
		info = vk.messages.getConversations(peer_id=2000000000+chat_id, count=1, random_id=get_random_id())["items"][0]["last_message"]["text"].split("\n")
		vk.messages.markAsRead(peer_id=2000000000+chat_id, mark_conversation_as_read=1, random_id=get_random_id())
		
		data["heal"] = int(info[2][info[2].find(":")+2::])
		data["lollipop"] = int(info[1][info[1].find(":")+2::])

		with open('JabkaData.json', 'w', encoding='utf-8') as f:
			dump(data, f, ensure_ascii=False, indent=4, sort_keys=True)
	except:
		return 1

def send_command(vk, command):
	try:
		vk.messages.send(chat_id=chat_id, message=commands[command], random_id=get_random_id())
		sleep(1)
		info = vk.messages.getConversations(peer_id=2000000000+chat_id, count=1, random_id=get_random_id())["items"][0]["last_message"]["text"].split("\n")
		vk.messages.markAsRead(peer_id=2000000000+chat_id, mark_conversation_as_read=1, random_id=get_random_id())
	except:
		return 1

def main():
	vk = login()
	
	if vk is None:
		print("Bad token")
	
	get_info(vk)

if __name__=='__main__':
	main()