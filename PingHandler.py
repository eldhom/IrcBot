import MessageHandler

class PingHandler(MessageHandler.MessageHandler):
	def __init__(self):
		super().__init__()
		
	def update(self, data):
		if data[1] == 'PING':
			self.addMessage(('PONG', data[2][0].replace('\r\n', '')))
			print('PING')
