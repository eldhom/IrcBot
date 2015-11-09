
import MessageHandler

class WolfpackRPGEngine(MessageHandler.MessageHandler):
	def __init__(self):
		self._queued 	= False
		self._inParty	= False
		self._isLeader	= False
		self._inQueueMessage = [
			'You have been placed in the Group Finder queue.\r\n',
			'You are already queued in the Group Finder! Type !queuetime for more information.\r\n',
		]
		self._removedFromQueueMessage = [
			'You were removed from the Group Finder.\r\n'
		]
		
	def onMessage(self, data):
		replyType 		= ''
		replyMessage	= ''
		nick	= data[0].split('!', 1)[0]
		message = data[2][1]
		if data[1] == 'WHISPER':
			if nick == 'lobotjr':
				if message in self._inQueueMessage:
					self._queued 	= True
				elif message in self._removedFromQueueMessage:
					self._queued	= False
			
				if not self._queued:
					replyType		= 'PRIVMSG'
					replyMessage 	= '#jtv :/w lobotjr !queue 1'
		return replyType, replyMessage
