import unicodedata
import IrcConnection
import time
import datetime
import WolfpackRPGEngine


class IrcBot:
	def __init__(self):
		self._connections 	= list()
		self._run 			= False
		self._whisperLog	= open('wlog.txt', 'a')
		self._rpgEngine		= WolfpackRPGEngine.WolfpackRPGEngine()
		
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
						if data[1] == 'PRIVMSG' or data[1] == 'WHISPER':
							nick = data[0].split('!', 1)[0]
							if data[1] == 'WHISPER':
								self._whisperLog.write(data[2][0] + ' ' + nick + ': ' + data[2][1])
								self._whisperLog.flush()
								sendMessage = self._rpgEngine.message(data)
								if sendMessage:
									con.sendMessage(sendMessage)
							try:
								timestamp = time.time()
								timestamp = datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
								print('[' + timestamp + '] ', end='')	#timestamp
								print(data[2][0] + ' ', end='') 		#channel
								print(nick + ': ', end='')						#nick
								print(data[2][1], end='')				#message
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