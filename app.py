# -*- coding: utf-8 -*-
import json
import vk_api
from conf import access_token, chat_id
from vk_api.utils import get_random_id
from time import sleep

commands = {
	"perks": "Моя жаба",
	"info": "Жаба инфо",
	"feed": "Покормить жабу",
	"mega_feed": "Откормить жабу",
	"invent": "Мой инвентарь",
	"heal": "Реанимировать жабу",
	"work": "Отправить жабу на работу",
	"end_work": "Завершить работу",
}

def login():
	"""login via token"""
	vk_session = vk_api.VkApi(token=access_token)
	vk = vk_session.get_api()
	return vk

def get_info(vk):
	"""send info command"""
	vk.messages.send(chat_id=chat_id, message=commands["perks"], random_id=get_random_id())
	info = vk.messages.getConversations(peer_id=2000000000+chat_id, count=1, random_id=get_random_id())["items"][0]["last_message"]["text"].split("\n")
	vk.messages.markAsRead(peer_id=2000000000+chat_id, mark_conversation_as_read=1, random_id=get_random_id())

	"""open and save data"""
	with open('JabkaData.json') as f:
		data = json.load(f)

	data["xp"] = int(info[2][info[2].find(":")+2:info[2].find("/"):])
	data["feel"] = info[7][info[7].find(":")+2::]
	data["level"] = int(info[1][info[1].find(":")+2::])
	data["money"] = int(info[5][info[5].find(":")+2::])
	data["status"] = info[4][info[4].find(":")+4::]

	vk.messages.send(chat_id=chat_id, message=commands["info"], random_id=get_random_id())
	sleep(1)
	info = vk.messages.getConversations(peer_id=2000000000+chat_id, count=1, random_id=get_random_id())["items"][0]["last_message"]["text"].split("\n")
	vk.messages.markAsRead(peer_id=2000000000+chat_id, mark_conversation_as_read=1, random_id=get_random_id())

	data["feed"] = info[0][info[0].find("з")+2::]
	data["work"] = info[2][info[2].find("з")+2::]
	if info[1].find("з") == -1:
		data["mega_feed"] = 0
	else:
		data["mega_feed"] = info[1][info[1].find("з")+2::]
	
	with open('JabkaData.json', 'w', encoding='utf-8') as f:
		json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True)

def main():
	vk = login()
	get_info(vk)

if __name__=='__main__':
	main()