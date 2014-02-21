import socket
import threading


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
			if data.find("PRIVMSG") != -1:
				try:
					IRC_PRIVMSG_Information = [
						data.split(':')[1].split('!')[0], #nick
						data.split('!')[1].split('@')[0], #user
						data.split('@')[1].split(' ')[0], #host
						data.split(' ')[2], #channel
						":".join(data.split(':')[2:]),
						True]
					if not IRC_PRIVMSG_Information[3][0] == '#':
						IRC_PRIVMSG_Information[5] = False
				except Exception as Error:
					 print("Error: " + Error)
				print(IRC_PRIVMSG_Information)
