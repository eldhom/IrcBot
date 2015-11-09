import IrcBot
import IrcConnection
import WhisperLog
import WolfpackRPGEngine
import OutputHandler
import PingHandler

f = open('pass.txt')
password = f.read()
f.close()
bot = IrcBot.IrcBot()

whisperCon = IrcConnection.IrcConnection('199.9.253.119', 6667)
whisperCon.login('Vassast', password)
whisperCon.sendMessage('CAP REQ :twitch.tv/commands')

channelCon = IrcConnection.IrcConnection('irc.twitch.tv', 6667)
channelCon.login('Vassast', password)
channelCon.joinChannel('#lobosjr')

bot.addMessageHandler(WhisperLog.WhisperLog('wlog.txt'))
bot.addMessageHandler(WolfpackRPGEngine.WolfpackRPGEngine())
bot.addMessageHandler(OutputHandler.OutputHandler())
bot.addMessageHandler(PingHandler.PingHandler())

bot.addConnection(whisperCon)
bot.addConnection(channelCon)

bot.run()