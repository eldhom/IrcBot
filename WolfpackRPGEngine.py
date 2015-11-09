
import MessageHandler

class WolfpackRPGEngine(MessageHandler.MessageHandler):
	def __init__(self):
		self._queued 	= False
		self._inParty	= False
		self._isLeader	= False
		self._inDungeon = False
		self._inQueueMessage = [
			'You have been placed in the Group Finder queue.\r\n',
			'You are already queued in the Group Finder! Type !queuetime for more information.\r\n',
			'You\'ve been matched for'
		]
		self._removedFromQueueMessage = [
			'You were removed from the Group Finder.\r\n',
			'Your party has been disbanded.\r\n'
		]
		
		self._inPartyMessage = [
			'You\'ve been matched for',
			'You already have a party created!'
		]
		
		self._leftPartyMessage = [
			'Your party has been disbanded.',
			'You left the party.'
		]
		
	def onMessage(self, data):
		replyType 		= ''
		replyMessage	= ''
		nick	= data[0].split('!', 1)[0]
		message = data[2][1]
		if data[1] == 'WHISPER':
			if nick == 'lobotjr':
				if not self._queued:
					for line in self._inQueueMessage:
						if message.find(line) != -1:
							self._queued = True
				else:
					for line in self._removedFromQueueMessage:
						if message.find(line) != -1:
							self._queued = False

				if not self._inParty:
					for line in self._inPartyMessage:
						if message.find(line) != -1:
							self._inParty = True
				else:
					for line in self._leftPartyMessage:
						if message.find(line) != -1:
							self._inParty = False
							self._isLeader = False
				
				if not self._inDungeon:
					if message.find('Successfully initiated') != -1:
						self._inDungeon = True
				else:
					if message.find('Dungeon complete.') != -1:
						self._inDungeon = False
						if self._isLeader:
							replyType 		= 'PRIVMSG'
							replyMessage	= '#jtv :/w lobotjr !start 1'
				if message.find('You are the party leader. Whisper me \'!start\' to begin!\r\n') != -1:
					self._isLeader = True
					replyType 		= 'PRIVMSG'
					replyMessage	= '#jtv :/w lobotjr !start 1'
					

			
				if not self._queued and not self._inParty:
					replyType		= 'PRIVMSG'
					replyMessage 	= '#jtv :/w lobotjr !queue 1'

		return replyType, replyMessage