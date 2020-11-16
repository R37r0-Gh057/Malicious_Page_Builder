import os, ctypes, subprocess
from datetime import datetime
from server import server
from time import sleep

YELLOW = '\033[33m'
BLUE = '\033[34m'
CYAN = '\033[36m'
GREEN = '\033[32;1m'
RED = '\033[31;1m'
WHITE = '\033[m'

banner = f'''
███╗   ███╗   ██╗        ██████╗ 
████╗ ████║   ██║        ██╔══██╗
██╔████╔██║   ██║        ██████╔╝
██║╚██╔╝██║   ██║        ██╔══██╗
██║ ╚═╝ ██║██╗███████╗██╗██████╔╝
╚═╝     ╚═╝╚═╝╚══════╝╚═╝╚═════╝ 

[*] {RED}Author: {WHITE}R37r0-Gh057
[*] {GREEN}Github: {WHITE}https://github.com/R37r0-Gh057
[*] {BLUE}Telegram: {WHITE}@R37R0_GH057
                                 '''

module_list = [] #for storing list of available modules
module_filename_list = [] #for storing filenames of available modules
module_desclist = [] #for storing description of available modules

class Page_Builder:
	def __init__(self,selected_modules):
		self.selected_modules = selected_modules #list of selected modules
		self.body = [] # <body> elements for the base HTML file
		self.src = [] # all <src> tags extracted from the selected modules are stored here for adding in the base HTML file
		self.funcs = [] # all function names extracted from the selected modules are stored here for adding in the base HTML file
		self.code = [] # all function codes extracted from the selected modules are stored here for adding the base HTML file.

	def extract_code(self,name): # Extracting function code from a module
		with open('templates/'+name,'r') as f:
			p = iter(f.read().split('\n'))
			for i in p:
				if i == '//MLB-START':
					while True:
						a = next(p,None)
						if a!= '//MLB-END':
							self.code.append(a.replace('//MLB-CALL',''))
						else:
							self.code.append('\n\n')
							break
					break

	def extract_src(self,name): # Extracting <src> tags from a module
		with open('templates/'+name,'r') as f:
			p = iter(f.read().split('\n'))
			for i in p:
				if i == '<!-- MLB_SRC -->':
					b = next(p,None)
					if not b in self.src:
						self.src.append(b)

	def extract_body(self,name): # Extracting required elements of the <body> tag from a module
		with open('templates/'+name,'r') as f:
			p = iter(f.read().split('\n'))
			for i in p:
				if i == '<!-- MLB-BODY -->':
					while True:
						a = next(p,None)
						if not '</body>' in a and not '<body>' in a:
							self.body.append(a)
						elif '</body>' in a:
							self.body.append('\n\n')
							break
					break

	def extract_function_name(self,name): # Extracting function names of a module
		with open('templates/'+name,'r') as f:
			p = iter(f.read().split('\n'))
			for i in p:
				if i=='//MLB-CALL':
					a = next(p,None)
					for i in a.strip().split(' '):
						if '()' in i:
							self.funcs.append(i.strip('{'))

	def build_page(self): # Calling all the above functions and bulding the base HTML file.

	'''
	Checking the number of selected modules is more than 1 or not,
	if it's more than 1 then the merging process will begin,
	if it;s not more than 1 then we simply run flask wtih the selected module as the base template.
	'''
		if len(self.selected_modules) != 1:
			for i in self.selected_modules:
				print_status('Extracting Code.'+YELLOW+f'[{i}]'+WHITE)
				self.extract_code(i)
				print_status('Extracting <script src.'+YELLOW+f'[{i}]'+WHITE)
				self.extract_src(i)
				print_status('Extracting body.'+YELLOW+f'[{i}]'+WHITE)
				self.extract_body(i)
				print_status('Extracting Function Names.'+YELLOW+f'[{i}]'+WHITE)
				self.extract_function_name(i)
			print_status('Merging Modules.')
			'''
			Writing the base HTML file:
			'''
			with open('templates/final.html','w') as f:
				f.write('<html>\n<head>\n')
				for i in self.src:
					f.write(i+'\n')
				f.write('</head>\n')
				f.write('<body>\n')
				for i in self.body:
					f.write(i+'\n')
				f.write('</body>\n')
				f.write('<script>\n')
				for i in self.code:
					f.write(i+'\n')
				a = ''
				for i in self.funcs:
					a+=i.strip()+'\nawait MLBsleep(2000);\n'
				f.write('''function MLBsleep(ms) {
						return new Promise(resolve => setTimeout(resolve, ms));
						}
async function mlb_launch() {
await MLBsleep(2000);
%s
					}
					'''%a.strip())
				f.write('\nmlb_launch();')
				f.write('\n</script>\n</html>')
			print_status('MERGED.')
		# Running the flask server
			server(5000,1) #
		else:
			server(5000,0,self.selected_modules[0])

'''
Loading modules by searching for 'MLBname' and 'MLBdesc' in every html file present in the 'templates/' directory
'''
def load_modules():
	global module_desclist, module_list
	for i in os.listdir('templates/'):
		if '.html' in i:
			with open('templates/'+i,'r') as f:
				a = False # Boolean variable for checking if MLBname was found or not
				b = False # Boolean variable for checking if MLBdesc was found or not
				for k in f.read().split('\n'):
					if 'MLBname=' in k:
						if not k.split('=')[1] in module_list:
							module_list.append(k.split('=')[1])
							a = True
						else:
							pass
					elif 'MLBdesc=' in k:
						if not k.split('=')[1] in module_desclist:
							module_desclist.append(k.split('=')[1])
							b = True
						else:
							pass
				if a and b: # If both the name and description are present, only then the module will be counted as valid
					module_filename_list.append(i)

	# Printing the number of valid modules:
	if len(module_list)!= 0:
		print_status(str(len(module_list))+' Modules Are Available to use.\n')
	else:
		print_err('No modules found.')
		exit()


'''
On windows, the above defined color codes don't get displayed in the console by default,
so we have to modify some values in the Registry.
'''
def win_color_config():
	if os.path.exists('c_done'):
		pass
	else:
		if ctypes.windll.shell32.IsUserAnAdmin() == 0:
			print_err('PLEASE RUN THIS SCRIPT AS ADMIN!')
			sleep(6)
			exit()
		else:
			subprocess.call('reg add HKEY_CURRENT_USER\\Console /v VirtualTerminalLevel /t REG_DWORD /d 0x00000001 /f',shell=True,stdout=subprocess.DEVNULL)
			with open('c_done', 'w') as f:
				f.write('done')

# These functions are for making printing easy:
def print_status(stuff):
	print(WHITE+'\n['+GREEN+"*"+WHITE+'] '+stuff)

def print_err(stuff):
	print(WHITE+'\n['+RED+'!'+WHITE+']'+RED+' ERROR: '+WHITE+stuff+'\n')

# For clearing the screen
def clear():
	if os.name == 'nt':
		subprocess.call('cls',shell=True)
	else:
		print(subprocess.getoutput('clear'))


# 'help' command output
def usage():
	print('\nCOMMAND\tDESCRIPTION\n')
	print('------ MENU COMMANDS ------\n')
	print(f'{RED}include\t{GREEN}include a module to build list. [include <module_name>]\n')
	print(f'{RED}exclude\t{GREEN}exclude a module from build list\n')
	print(f'{RED}list\t{GREEN}list available modules.\n')
	print(f'{RED}list_selected\t{GREEN}list selected modules.\n')
	print(f'{RED}build\t{GREEN}build link with the selected modules.\n')
	print(f'{RED}help\t{GREEN}show this help message.\n')
	print(f'{RED}clear\t{GREEN}clear the screen.\n')
	print(f'{RED}exit\t{GREEN}does what it says.\n')


# User Interface
def menu():
	selected_modules = []
	selected_modules_names = []
	while True:
		x = input(WHITE+'{'+RED+'M.L.B '+WHITE+'}: ')
		if x.lower() == 'list':
			print(CYAN+'\n\t--AVAILABLE MODULES--\t\n'+WHITE)
			c = 1
			for i in module_list:
				print(WHITE+str(c)+'. '+YELLOW+i.replace('html','')+'\t'+GREEN+module_desclist[c-1]+'\n'+WHITE)
				c+=1
		elif x.lower() == 'list_selected':
			if len(selected_modules) != 0:
				c = 1
				print(CYAN+'\n\t--- Selected Modules---:\n '+WHITE)
				for i in selected_modules_names:
					print(WHITE+str(c)+'. '+YELLOW+i)
					c+=1
				print('\n')

			else:
				print_status('No modules selected.')
		elif x.lower() == 'exit':
			exit()

		elif x.lower() == 'help':
			usage()

		elif x.lower() == 'clear':
			clear()
		elif 'include' in x.lower():
			if len(x.split(' ')) == 2:
				if x.split(' ')[1] in selected_modules_names:
					print_err('Module is already present in the list.')
				else:
					if x.split(' ')[1] in module_list:
						c = 0
						for i in module_list:
							if i == x.split(' ')[1]:
								break
							else:
								c+=1
						print_status('Adding '+YELLOW+x.split(' ')[1]+WHITE+' to build list.\n')
						selected_modules.append(module_filename_list[c])
						selected_modules_names.append(x.split(' ')[1])
						#selected_modules.append(x.split(' ')[1])
					else:
						print_err('Invalid Module Selected')
			else:
				print_err('Invalid syntax. Type "help".')

		elif 'exclude' in x.lower():
			if len(x.split(' ')) == 2:
				if x.split(' ')[1] in selected_modules_names:
					c = 0
					for i in selected_modules_names:
						for k in module_list:
							if i == k:
								break
							else:
								c+=1
						break
					selected_modules.remove(module_filename_list[c])
					selected_modules_names.remove(x.split(' ')[1])
					print_status(YELLOW+x.split(' ')[1]+WHITE+' removed from list\n')
				else:
					print_err('Specified module is not in the list.')
			else:
				print_err('Invalid syntax. Type "help".')
		elif x.lower() == 'build':
			if len(selected_modules) != 0:
				Page_Builder(selected_modules).build_page()
			else:
				print_err('No module selected for building.')
		elif x == 'fuck':
			print(selected_modules)
		else:
			print_err('Invalid command. Type "help" for a list of commands.')


try:
	# Checking if the platform is Windows, and if is then we call win_color_config()
	if os.name == 'nt':
		win_color_config()
	print(banner+'\n\n')
	load_modules()
	menu()
except Exception as e:
	with open('error.txt','a') as f:
		f.write(datetime.now().strftime('%Y_%m_%d-%H_%M_%S')+' : '+str(e)+'\n\n') # Logging errors
	print_err(e)
	exit()