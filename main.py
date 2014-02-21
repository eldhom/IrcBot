import IrcBot

bot = IrcBot.IrcBot('irc.twitch.tv', 6667)
if bot.login('NICK', 'PASS') == True:
	bot.joinChannel('CHANNEL')
	
	def FrankerZ(msgtype, msg, nick):
		bot.sendMessage('FrankerZ')
	
	def hello(msgtype, msg, nick):
		bot.sendMessage('Hello ' + nick)

	bot.addMsgHandler(hello, '!Hello')
	bot.addMsgHandler(FrankerZ, 'FrankerZ')
	bot.run()	
