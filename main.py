import IrcBot

bot = IrcBot.IrcBot('irc.twitch.tv', 6667)
if bot.login('NICK', 'PASS') == True:
	bot.joinChannel('#eldhom')
	
	def FrankerZ(msgtype, msg, nick):
		bot.sendMessage('FrankerZ')

	bot.addMsgHandler(FrankerZ, 'FrankerZ')
	bot.run()	
