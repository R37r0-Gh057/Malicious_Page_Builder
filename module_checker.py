from os import listdir, path
from sys import argv

YELLOW = '\033[33m'
GREEN = '\033[32;1m'
CYAN = '\033[36m'
RED = '\033[31;1m'
WHITE = '\033[m'

def extract_name(file,par=1):
	if par == 1:
		with open('templates/'+file,'r') as f:
			for i in f.read().split('\n'):
				if 'MLBname=' in i:
					return i.split('=')[1]
	else:
		with open(file,'r') as f:
			for i in f.read().split('\n'):
				if 'MLBname=' in i:
					return i.split('=')[1]

def extract_function_name(name,par=1):
	a = []
	if par == 1:
		with open('templates/'+name,'r') as f:
			p = iter(f.read().split('\n'))
			for i in p:
				if i=='//MLB-CALL':
					a.append(next(p,None).strip().split(' ')[1])
			return a
	else:
		with open(name,'r') as f:
			p = iter(f.read().split('\n'))
			for i in p:
				if i=='//MLB-CALL':
					b = next(p,None)
					for i in b.strip().split(' '):
						if '()' in i:
							a.append(i.strip('{'))
			return a


def help():
	print('USAGE: python3 module_checker.py <path_to_your_module.py>')
	exit()

def main(file):
	D = False
	if path.isfile(file):
		a = extract_function_name(file,0)
		c = extract_name(file,0)
		for i in listdir('templates/'):
			if not i in file and i!='final.html':
				d = extract_name(i)
				if c == d:
					print(f'\n[{CYAN}{d}{WHITE}] MODULE NAME is already in use by {YELLOW}{i}:{d}{WHITE} module.')
					if not D:
						D = True
				for k in extract_function_name(i):
					if k in a:
						print(f'\n[{CYAN}{k}{WHITE}] FUNCTION NAME is already in use by {YELLOW}{d}:{i}{WHITE} module.')
						if not D:
							D = True
		if not D:
			print(GREEN+'ALL GOOD.')
		input()
	else:
		print(RED+"ERROR: "+WHITE+"Specified File Not Found."+WHITE)
		exit()
if len(argv) < 2:
	main(input('enter path to your module.py: '))
elif len(argv) > 2:
	help()
elif len(argv) == 2:
	main(argv[1])