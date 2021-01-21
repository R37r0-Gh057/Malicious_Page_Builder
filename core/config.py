def init():
	global YELLOW, WHITE, CYAN, RED, GREEN, BLUE, banner, module_desc_list, module_list, module_filename_list

	YELLOW = '\033[33m'
	BLUE = '\033[34m'
	CYAN = '\033[36m'
	GREEN = '\033[32;1m'
	RED = '\033[31;1m'
	WHITE = '\033[m'

	module_list = [] #for storing list of available modules
	module_filename_list = [] #for storing filenames of available modules
	module_desc_list = [] #for storing description of available modules


	banner = f'''
███╗   ███╗   ██████╗ ██████╗ 
████╗ ████║   ██╔══██╗██╔══██╗
██╔████╔██║   ██████╔╝██████╔╝
██║╚██╔╝██║   ██╔═══╝ ██╔══██╗
██║ ╚═╝ ██║██╗██║██╗  ██████╔╝
╚═╝     ╚═╝╚═╝╚═╝╚═╝  ╚═════╝ 
                               
                               
[*] {RED}Author: {WHITE}R37r0-Gh057
[*] {GREEN}Github: {WHITE}https://github.com/R37r0-Gh057
[*] {BLUE}Telegram: {WHITE}@R37R0_GH057
                                 '''
