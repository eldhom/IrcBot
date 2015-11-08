import unicodedata
import IrcConnection
import time
import datetime


class IrcBot:
	def __init__(self):
		self._connections = list()
		self._run = False
		
	def addConnection(self, con):
		self._connections.append(con)
	
	def run(self):
		self._run = True
		for con in self._connections:
			con.start()
			
		while self._run:
			try:
				for con in self._connections:
					data = con.getData()
					if not data:
						continue
					try:
						if data[1] == 'PRIVMSG':
							nick = data[0][1:].split('!', 1)[0]
							try:
								timestamp = time.time()
								timestamp = datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
								print('[' + timestamp + '] ', end='')
								print(data[2][0] + ' ', end='')
								print(nick, end='')							
								print(': ', end='')
								print(data[2][1], end='')
							except UnicodeEncodeError:
								print(unicodedata.normalize('NFKD', data[3]).encode('ascii', 'ignore'), end='')
								print(': ', end='')
								print(unicodedata.normalize('NFKD', data[2][1]).encode('ascii', 'ignore') + '\r\n', end='')
						elif data[1] == 'PING':
							reply = 'PONG ' + data[2][0]
							con.sendMessage(reply)
							print(reply, end='')
					except IndexError:
						pass						
			except KeyboardInterrupt:
				for con in self._connections:
					con.logout()
				self._run = False
		for con in self._connections:
			con.join()