<<<<<<< HEAD
class IrcMessage:
=======



class IrcMsg:
>>>>>>> a763ab8c0c0a70e74905dcf9ac3f3889d7cc9b8b
	def __init__(self, data):
		self.type = data.split(' ')[1]
		if self.type == 'PRIVMSG':
			self.body = data.split(':')[2][:-2]
			self.nick = data.split(':')[1].split('!')[0].strip()
		elif self.type == 'MODE':
			self.channel 	= data.split(' ')[2]
			self.mode		= data.split(' ')[3]
			self.nick		= data.split(' ')[4][:-2]
