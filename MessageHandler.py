

class MessageHandler:
	def __init__(self):
		self._messageQueue = list()
	
	def update(self, data):
		pass
		
	def addMessage(self, message):
		self._messageQueue.append(message)
		
	def getMessage(self):
		if not self._messageQueue:
			return False
		return self._messageQueue.pop(0)
