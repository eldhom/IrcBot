
class WolfpackRPGEngine:
	def __init__(self):
		self._queued = False
		self._inQueueMessage = [
			'You have been placed in the Group Finder queue.\r\n',
			'You are already queued in the Group Finder! Type !queuetime for more information.\r\n',
		]
		self._removedFromQueueMessage = [
			'You were removed from the Group Finder.\r\n'
		]
		
	def message(self, d):
		value 	= False
		nick	= d[0].split('!', 1)[0]
		message = d[2][1]
		if nick == 'lobotjr':
			if message in self._inQueueMessage:
				self._queued 	= True
			elif message in self._removedFromQueueMessage:
				self._queued	= False
			
			if not self._queued:
				value = 'PRIVMSG #jtv :/w lobotjr !queue 1'
		return value
