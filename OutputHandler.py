import MessageHandler
import time
import datetime
import unicodedata


class OutputHandler(MessageHandler.MessageHandler):
	def __init_():
		super().__init__()
	
	def update(self, data):	
		if data[1] == 'WHISPER':
			nick = data[0].split('!', 1)[0]
			timestamp = time.time()
			timestamp = datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
			print('[' + timestamp + '] ', end='')	#timestamp
			try:
				print(data[2][0] + ' ', end='') 		#channel
				print(nick + ': ', end='')				#nick
				print(data[2][1], end='')				#message
			except UnicodeEncodeError:
				print(unicodedata.normalize('NFKD', data[2][0]).encode('ascii', 'ignore'), end='')
				print(unicodedata.normalize('NFKD', nick + ': ').encode('ascii', 'ignore'), end='')
				print(unicodedata.normalize('NFKD', data[2][1] + '\r\n').encode('ascii', 'ignore'), end='')
		
		