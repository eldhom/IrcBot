import IrcBot

bot = IrcBot.IrcBot('irc.twitch.tv', 6667)
if bot.login('EldhBot', 'oauth:ipm5kf729ao4y15tq27si9oix2ft35n') == True:
	bot.joinChannel('#eldhom')
	
	def FrankerZ(msgtype, msg, nick):
		if bot.isMod(nick):
			bot.sendMessage('FrankerZ')
	
	def hello(msgtype, msg, nick):
		bot.sendMessage('Hello ' + nick)

	bot.addMsgHandler(hello, '!Hello')
	bot.addMsgHandler(FrankerZ, 'FrankerZ')
	bot.run()	
