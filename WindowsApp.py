import sys
sys.path.append("./utility_code")

import PySimpleGUIQt as sg
from tray_functions import start_JabkaBot, refresh_data
from multiprocessing import Process, current_process

menu_def = ['BLANK', ['&Start JabkaBot', '&Refresh data', '&Exit']]

tray = sg.SystemTray(menu=menu_def, filename='images/icon.png')

while True:
	menu_item = tray.Read()
	print(menu_item)
	if menu_item == 'Exit':
		break
	elif menu_item == 'Start JabkaBot':
		menu_def = ['BLANK', ['Stop JabkaBot', 'Refresh data', 'Exit']]
		tray.Update(menu=menu_def, filename='images/icon.png')
		
		start_JabkaBot()
	elif menu_item == 'Refresh data':
		refresh_data()
	elif menu_item == 'Stop JabkaBot':
		menu_def = ['BLANK', ['Start JabkaBot', 'Refresh data', 'Exit']]
		tray.Update(menu=menu_def, filename='images/icon.png')
		
		start_JabkaBot()