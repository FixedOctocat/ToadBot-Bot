import sys
sys.path.append("./utility_code")

import PySimpleGUIQt as sg
from tray_functions import start_JabkaBot, refresh_data
from multiprocessing import Process, current_process

def main():
	#system tray creation
	menu_def = ['BLANK', ['&Start JabkaBot', '&Refresh data', '&Exit']]
	tray = sg.SystemTray(menu=menu_def, filename='images/icon.png')

	while True:
		menu_item = tray.Read()
		
		if menu_item == 'Exit':
			#end JabkaBot process
			try:
				JabkaBot.terminate()
				JabkaBot.join()
			except:
				pass

			#end RefreshData process
			try:
				RefreshData.terminate()
				RefreshData.join()
			except:
				pass

			#quit
			break
		elif menu_item == 'Start JabkaBot':
			#edit menu
			menu_def = ['BLANK', ['Stop JabkaBot', 'Refresh data', 'Exit']]
			tray.Update(menu=menu_def)
			
			#show notification
			tray.ShowMessage("JabkaBot", "Жабкабот следит за Вашей жабкой", time=10)
			
			#start process
			JabkaBot = Process(target=start_JabkaBot)
			JabkaBot.start()
		elif menu_item == 'Refresh data':
			#show notification
			tray.ShowMessage("JabkaBot", "Обновляем данные...", time=10)
			
			#start process
			RefreshData = Process(target=refresh_data())
			RefreshData.start()
		elif menu_item == 'Stop JabkaBot':
			#edit menu
			menu_def = ['BLANK', ['Start JabkaBot', 'Refresh data', 'Exit']]
			tray.Update(menu=menu_def)
			
			#show notification
			tray.ShowMessage("JabkaBot", "Жабкабот больше не следит за жабкой", time=10)

			#end process
			JabkaBot.terminate()
			JabkaBot.join()

if __name__ == '__main__':
	main()