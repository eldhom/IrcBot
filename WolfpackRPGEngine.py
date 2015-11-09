
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
			'You were removed from the Group Finder.\r\n',
			'Your party has been disbanded.\r\n'
		]
		
		self._inPartyMessage = [
			'You\'ve been matched for'
		]
		
		self._disbandPartyMessage = [
			'Your party has been disbanded.'
		]
		
	def onMessage(self, data):
		replyType 		= ''
		replyMessage	= ''
		nick	= data[0].split('!', 1)[0]
		message = data[2][1]
		if data[1] == 'WHISPER':
			if nick == 'lobotjr':
				for line in self._inQueueMessage:
					if message.find(line) != -1:
						self._queued = True
				for line in self._removedFromQueueMessage:
					if message.find(line) != -1:
						self._queued = False

				for line in self._inPartyMessage:
					if message.find(line) != -1:
						self._inParty = True
				for line in self._disbandPartyMessage:
					if message.find(line) != -1:
						self._inParty = False
			
				if not self._queued:
					replyType		= 'PRIVMSG'
					replyMessage 	= '#jtv :/w lobotjr !queue 1'

		return replyType, replyMessage
