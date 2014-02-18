import IrcBot

bot = IrcBot.IrcBot('irc.twitch.tv', 6667)
if bot.login('EldhBot', 'oauth:ipm5kf729ao4y15tq27si9oix2ft35n') == True:
	bot.joinChannel('#eldhom')
	
	def FrankerZ(msgtype, msg, nick):
		bot.sendMessage('FrankerZ')

	bot.addMsgHandler(FrankerZ, 'FrankerZ')
	bot.run()	
