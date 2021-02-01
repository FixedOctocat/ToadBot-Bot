from webbrowser import open_new
from app import main
from conf import token_url
from vk_connect import login, get_info

def start_JabkaBot():
	vk = login()
		
	if vk is None:
		open_new(token_url)
		exit()
	elif vk == 1:
		return 1

	main(vk)

def refresh_data():
	vk = login()
		
	if vk is None:
		open_new(token_url)
		exit()
	elif vk == 1:
		return 1

	get_info(vk)
