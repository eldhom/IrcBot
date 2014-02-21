import socket
import threading

class IrcMsg:
	def __init__(self, data):
		self.type = data.split(' ')[1]
		if self.type == 'PRIVMSG':
			self.body = data.split(':')[2][:-2]
			self.nick = data.split(':')[1].split('!')[0]
		elif self.type == 'JOIN':
			self.nick = data.split(':')[1].split('!')[0]
		elif self.type == 'PART':
			self.nick = data.split(':')[1].split('!')[0]
		elif self.type == 'MODE':
			self.channel 	= data.split(' ')[2]
			self.mode		= data.split(' ')[3]
			self.nick		= data.split(' ')[4][:-2]

class MsgHandler:
	def __init__(self, function, msg):
		self.function 	= function
		self.msg		= msg

class IrcBot:
	def __init__(self, server, port):
		self.msg_handlers 		= []
		self.raw_msg_functions	= []
		self.mods				= []
		self.users				= []
		self.server = server
		self.port	= port
		self.socket	= socket.socket()
		self.socket.connect((server, port))
		self._connected = True
	
	def login(self, nick, password):
		self.nick		= nick
		self.password	= password
		self.socket.send(str('PASS ' + self.password + '\r\n').encode('UTF-8'))
		self.socket.send(str('NICK ' + self.nick + '\r\n').encode('UTF-8'))
		data = str(self.socket.recv(4096), 'UTF-8')
		print(data)
		if data.find('unsuccessful') != -1:
			self._loggedin = False
		else:
			self._loggedin = True
		return self._loggedin
		
	def joinChannel(self, channel):
		self.channel = channel
		self.socket.send(str('JOIN ' + self.channel + '\r\n').encode('UTF-8'))
		data = str(self.socket.recv(4096), 'UTF-8')
		print(data)

		
	def addMsgHandler(self, function, msg):
		self.msg_handlers.append(MsgHandler(function, msg))

	def addRawMsgFunction(self, function):
		self.raw_msg_functions.append(function)
	
	def sendMessage(self, message):
		self.socket.send(str('PRIVMSG ' + self.channel + ' :'+ message + '\r\n').encode('UTF-8'))
		print('SENT:  ' + message)
	
	def sendRawMessage(self, message):
		self.socket.send(message.encode('UTF-8'))

	def isMod(self, nick):
		if nick in self.mods:
			return True
		else:
			return False
	
	def run(self):
		threading.Thread(target=self._loop()).start()
		
	def _loop(self):
		while self._loggedin:
			data = str(self.socket.recv(4096), 'UTF-8')
			print(data)
			if(data != "PING\r\n"):
				for raw_msg_function in self.raw_msg_functions:
					raw_msg_function(data)
				msg = IrcMsg(data)
				if msg.type == 'PRIVMSG':
					if msg.nick not in self.users:
						self.users.append(msg.nick)
					for msg_handler in self.msg_handlers:
						if msg.body == msg_handler.msg:
							msg_handler.function(msg.type, msg.body, msg.nick)
				elif msg.type == 'JOIN':
					if msg.nick not in  self.users:
						print(msg.nick + ' joined')
						self.users.append(msg.nick)
				elif msg.type == 'PART':
					if msg.nick in self.users:
						print(msg.nick + ' parted')
						list(filter(msg.nick.__ne__, self.users))
				elif msg.type == 'MODE':
					print('Modechange')
					if msg.mode == '+o':
						if msg.nick not in self.mods:
							print(msg.nick + ' is now mod')
							self.mods.append(msg.nick)
					elif msg.mode == '-o':
						if msg.nick in self.mods:
							list(filter(msg.nick.__ne__, self.mods))
			else:
				print('ping')
				self.socket.send(str(data.replace('PING', 'PONG')).encode('UTF-8'))
