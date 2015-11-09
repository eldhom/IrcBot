import time
import MessageHandler

class WolfpackRPGEngine(MessageHandler.MessageHandler):
	def __init__(self):
		super().__init__()
		self._queued 	= False
		self._inParty	= False
		self._isLeader	= False
		self._inDungeon = False
		self._messageQueue 		= list()
		self._checkLevelTimer 	= 0
		self._startTime			= time.time()
		self._endTime			= 0
		self._level				= 0
		
		self._inQueueMessage = [
			'You have been placed in the Group Finder queue.\r\n',
			'You are already queued in the Group Finder! Type !queuetime for more information.\r\n',
		]
		self._removedFromQueueMessage = [
			'You were removed from the Group Finder.\r\n',
			'Your party has been disbanded.\r\n',
			'You\'ve been matched for'
		]
		
		self._inPartyMessage = [
			'You\'ve been matched for',
			'You already have a party created!'
		]
		
		self._leftPartyMessage = [
			'Your party has been disbanded.',
			'You left the party.'
		]
			
	def update(self, data):
		nick	= data[0].split('!', 1)[0]
		message = data[2][1]
		if data[1] == 'WHISPER':
			if nick == 'lobotjr':
				if message.find('You are a Level') != -1:
					self._level = int(message.split()[4])
					
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
							self.addMessage(('PRIVMSG', '#jtv :/w lobotjr !start 1'))

				if message.find('You are the party leader. Whisper me \'!start\' to begin!\r\n') != -1:
					self._isLeader = True
					self.addMessage(('PRIVMSG', '#jtv :/w lobotjr !start ' + self.getRecDungeon()))
			
				if not self._queued and not self._inParty:
					self.addMessage(('PRIVMSG', '#jtv :/w lobotjr !queue ' + self.getRecDungeon()))
				

		self._endTime = time.time()
		self._checkLevelTimer -= self._endTime - self._startTime
		self._startTime = self._endTime
		if self._checkLevelTimer <= 0:
			self.addMessage(('PRIVMSG', '#jtv :/w lobotjr !xp'))
			self._checkLevelTimer = 120
	
	def getRecDungeon(self):
		if self._level == 3:
			return '1'
		elif self._level == 4:
			return '2'
		elif self._level == 5:
			return '3'
		elif self._level == 6:
			return '4'
		elif self._level == 7:
			return '5'
		elif self._level == 8:
			return '6'
		else:
			return '7'