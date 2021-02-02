import os, subprocess, socket, ctypes
from . import config

def is_connected():
	try:
		socket.create_connection(('1.1.1.1',53))
		return True
	except:
		return False
'''
On windows, the above defined color codes don't get displayed in the console by default,
so we have to modify some values in the Registry.
'''
def win_color_config():
	if os.path.exists('c_done'):
		pass
	else:
		if ctypes.windll.shell32.IsUserAnAdmin() == 0:
			print('PLEASE RUN THIS SCRIPT AS ADMIN FOR ONCE!')
			sleep(6)
			exit()
		else:
			subprocess.call('reg add HKEY_CURRENT_USER\\Console /v VirtualTerminalLevel /t REG_DWORD /d 0x00000001 /f',shell=True,stdout=subprocess.DEVNULL)
			with open('c_done', 'w') as f:
				f.write('done')

def print_status(stuff):
	print(config.WHITE+'\n['+config.GREEN+"*"+config.WHITE+'] '+str(stuff))

def print_err(stuff):
	print(config.WHITE+'\n['+config.RED+'!'+config.WHITE+']'+config.RED+' ERROR: '+config.WHITE+(stuff)+'\n')

# For clearing the screen
def clear():
	if os.name == 'nt':
		subprocess.call('cls',shell=True)
	else:
		print(subprocess.getoutput('clear'))

'''
Loading modules by searching for 'MLBname' and 'MLBdesc' in every html file present in the 'templates/' directory
'''
def load_modules():
	if os.path.isfile('core/templates/final.html'):
		os.remove('core/templates/final.html')
	for i in os.listdir('core/templates/'):
		if '.html' in i:
			with open('core/templates/'+i,'r') as f:
				a = False # Boolean variable for checking if MLBname was found or not
				b = False # Boolean variable for checking if MLBdesc was found or not
				for k in f.read().split('\n'):
					if 'MLBname=' in k:
						if not k.split('=')[1] in config.module_list:
							config.module_list.append(k.split('=')[1])
							a = True
						else:
							pass
					elif 'MLBdesc=' in k:
						if not k.split('=')[1] in config.module_desc_list:
							config.module_desc_list.append(k.split('=')[1])
							b = True
						else:
							pass
				if a and b: # If both the name and description are present, only then the module will be counted as valid
					config.module_filename_list.append(i)

	# Printing the number of valid modules:
	if len(config.module_list)!= 0:
		print_status(str(len(config.module_list))+' Modules Are Available to use.\n')
	else:
		print_err('No modules found.')
		exit()

# 'help' command output
def usage():
	print('\nCOMMAND\tDESCRIPTION\n')
	print('------ MENU COMMANDS ------\n')
	print(f'{config.RED}include\t{config.GREEN}include a module to build list. [include <module_name>]\n')
	print(f'{config.RED}exclude\t{config.GREEN}exclude a module from build list\n')
	print(f'{config.RED}list\t{config.GREEN}list available modules.\n')
	print(f'{config.RED}list_selected\t{config.GREEN}list selected modules.\n')
	print(f'{config.RED}build\t{config.GREEN}build link with the selected modules.\n')
	print(f'{config.RED}help\t{config.GREEN}show this help message.\n')
	print(f'{config.RED}clear\t{config.GREEN}clear the screen.\n')
	print(f'{config.RED}exit\t{config.GREEN}does what it says.\n')

