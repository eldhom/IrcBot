import IrcConnection
import WolfpackRPGEngine
import MessageHandler


class IrcBot:
	def __init__(self):
		self._connections 		= list()
		self._messageHandlers	= list()
		self._run 				= False
		self._rpgEngine			= WolfpackRPGEngine.WolfpackRPGEngine()
		
	def addConnection(self, con):
		self._connections.append(con)
	
	def addMessageHandler(self, handler):
		self._messageHandlers.append(handler)
	
	def run(self):
		self._run = True
		for con in self._connections:
			con.start()
		try:
			while self._run:
				for con in self._connections:
					data = con.getData()
					if data:
						try:
							for handler in self._messageHandlers:
								handler.update(data)
								replyMessage = handler.getMessage()
								if replyMessage:
									print(replyMessage[0] + ' ' + replyMessage[1])
									con.sendMessage(replyMessage[0] + ' ' + replyMessage[1])
							if data[1] == 'PING':
								reply = 'PONG ' + data[2][0]
								con.sendMessage(reply)
								print(reply, end='')
						except IndexError:
							pass						
			
			for con in self._connections:
				con.join()
		except KeyboardInterrupt:
				for con in self._connections:
					con.logout()
				self._run = False
				for con in self._connections:
					con.join()