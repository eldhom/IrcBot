import socket
import time
import threading

class IrcConnection(threading.Thread):
	def __init__(self, server, port):
		super(IrcConnection, self).__init__()
		self._server 	= server
		self._port		= port
		self._socket	= socket.socket()
		self._socket.settimeout(5)
		self._socket.connect((server, port))
		self._channels 	= list()
		self._time		= 0
	
	def login(self, user, password):
		self._user		= user
		self._password	= password
		self._socket.send(str('PASS ' + self._password + '\r\n').encode('UTF-8'))
		self._socket.send(str('NICK ' + self._user + '\r\n').encode('UTF-8'))
		data = str(self._socket.recv(4096), 'UTF-8')
		print(data)
		if data.find('unsuccessful') != -1:
			self._loggedIn = False
		else:
			self._loggedIn = True
		return self._loggedIn
	
	def logout(self):
		self._loggedIn = False
	
	def joinChannel(self, channel):
		self._channels.append(channel)
		self._socket.send(str('JOIN ' + channel + '\r\n').encode('UTF-8'))
		data = str(self._socket.recv(4096), 'UTF-8')
		print(data)
	
	def getChannels(self):
		return self._channels
	
	def parseData(self, s):
		prefix 		= ''
		trailing 	= []
		nick 		= ''
		command 	= ''
		
		if not s:
			raise Exception("Empty line.")
		if s[0] == ':':
			prefix, s = s[1:].split(' ', 1)
		if s.find(' :') != -1:
			s, trailing = s.split(' :', 1)
			args = s.split()
			args.append(trailing)
		else:
			args = s.split()
		command = args.pop(0)
		return prefix, command, args
		
	def sendMessage(self, message):
		if message.find('\r\n') == -1:
			message += '\r\n'
		self._socket.send((message).encode('UTF-8'))
	
	def getData(self):
		if not self._messages:
			return False
		return self._messages.pop(0)

	def resetPingTime(self):
		self._time = 120
		
	def connect(self):
		pass
	
	def run(self):
		self._messages 	= list()
		self.resetPingTime()
		while self._loggedIn:
			try:
				data = str(self._socket.recv(4096), 'UTF-8')
				self._messages.append(self.parseData(data))
			except (socket.timeout, Exception):
				continue