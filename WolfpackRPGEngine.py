import Timer
import MessageHandler
import json
import urllib.request

class WolfpackRPGEngine(MessageHandler.MessageHandler):
	def __init__(self):
		super().__init__()
		self._queued 	= False
		self._inParty	= False
		self._isLeader	= False
		self._inDungeon = False
		self._messageQueue 		= list()
		self._syncTimer	= Timer.Timer(0)
		self._checkStreamTimer	= Timer.Timer(60)
		self._updateCoinsTimer	= Timer.Timer()
		self._streamLive		= False
		self._level				= 0
		self._coins				= 0
		
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
		if data[1] == 'WHISPER':
			nick	= data[0].split('!', 1)[0]
			message = data[2][1]
			if nick == 'lobotjr':
				if 'You are a Level' in message:
					self._level = int(message.split()[4])
					self._syncTimer.start(7200)
				if 'You have:' in message:
					self._coins = int(message.split()[2])
					self._syncTimer.start(7200)
				
				if 'DING!' in message:
					self._level += 1
						
				if 'you\'ve earned' in message:
					self._coins += int(message.split()[6])
					
				if self.canJoinDungeon():
					if not self._queued:
						for line in self._inQueueMessage:
							if line in message:
								self._queued = True
					else:
						for line in self._removedFromQueueMessage:
							if line in message:
								self._queued = False

					if not self._inParty:
						for line in self._inPartyMessage:
							if line in message:
								self._inParty = True
					else:
						for line in self._leftPartyMessage:
							if line in message:
								self._inParty = False
								self._isLeader = False
				
					if not self._inDungeon:
						if 'Successfully initiated' in message:
							self._inDungeon = True
							self._coins -= 50+10*(self._level-3)
					else:
						if 'Dungeon complete.' in message:
							self._inDungeon = False
							if self._isLeader:
								self.addMessage(('PRIVMSG', '#jtv :/w lobotjr !start 1'))
					

					if 'You are the party leader. Whisper me \'!start\' to begin!\r\n' in message:
						self._isLeader = True
						self.addMessage(('PRIVMSG', '#jtv :/w lobotjr !start ' + self.getRecDungeon()))
			
					if not self._queued and not self._inParty:
						self.addMessage(('PRIVMSG', '#jtv :/w lobotjr !queue ' + self.getRecDungeon()))
				

		if self._syncTimer.isDone():
			self.addMessage(('PRIVMSG', '#jtv :/w lobotjr !stats'))
			self._syncTimer.start(600)
		if self._checkStreamTimer.isDone():
			self._checkStream()
			self._checkStreamTimer.start(60)
		if self._streamLive and self._updateCoinsTimer.isDone():
			self._updateCoins()
			self._updateCoinsTimer.start(1800)
			
	def _checkStream(self):
		html = ""
		with urllib.request.urlopen('https://api.twitch.tv/kraken/streams/lobosjr') as response:
			html = response.read().decode('utf-8')
		
		data = json.loads(html)
		if data['stream']:
			self._streamLive = True
			self._updateCoinsTimer.start(1800)
			print('Lobosjr went online \o/\r\n', end='')
		if not data['stream'] and  self._streamLive:
			self._streamLive = False
			print('Stream went offline :(\r\n', end='')
	
	def _updateCoins(self):
		self._coins += 3
		print('Gained 3 coins')
	
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
	
	def canJoinDungeon(self):
		if self._level == 0:
			return False
		if self._coins > 50 + 10*(self._level -3):
			return True
	
