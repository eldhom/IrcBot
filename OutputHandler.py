import MessageHandler
import time
import datetime
import unicodedata


class OutputHandler(MessageHandler.MessageHandler):
	def __init_():
		pass
	
	def onMessage(self, data):
		replyType 		= ''
		replyMessage	= ''
		
		if data[1] == 'PRIVMSG' or data[1] == 'WHISPER':
			nick = data[0].split('!', 1)[0]
			try:
				timestamp = time.time()
				timestamp = datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
				print('[' + timestamp + '] ', end='')	#timestamp
				print(data[2][0] + ' ', end='') 		#channel
				print(nick + ': ', end='')				#nick
				print(data[2][1], end='')				#message
			except UnicodeEncodeError:
				print(unicodedata.normalize('NFKD', data[3]).encode('ascii', 'ignore'), end='')
				print(': ', end='')
				print(unicodedata.normalize('NFKD', data[2][1]).encode('ascii', 'ignore') + '\r\n', end='')
		
		return replyType, replyMessage
		