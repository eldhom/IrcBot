
import MessageHandler

class WhisperLog(MessageHandler.MessageHandler):
	def __init__(self, fileName):
		self._fileName		= fileName
		self._uniqueLines 	= list()
		try:
			with open('unique'+fileName, 'r') as f:
				self._uniqueLines = f.read().splitlines()
			self._uniqueLines = [i for i in self._uniqueLines if i !='']
			for i, line in enumerate(self._uniqueLines):
				self._uniqueLines[i] += '\r\n'
		except FileNotFoundError:
			pass

	def onMessage(self, data):
		replyType 		= ''
		replyMessage	= ''
		if data[1] == 'WHISPER':
			nick	= data[0].split('!', 1)[0]
			message = data[2][0] + ' ' + nick + ': ' + data[2][1]
			if message not in self._uniqueLines:
				self._uniqueLines.append(message)
				with open('unique' + self._fileName, 'a') as f:
					f.write(message)
			with open(self._fileName, 'a') as f:
				f.write(message)
		return replyType, replyMessage