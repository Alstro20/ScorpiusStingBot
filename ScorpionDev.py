import discord # Main Discord API
import asyncio 
import cat #Random cat api
import os #OS API to create/delete files
import time
import requests
from threading import Thread
#allows import of other python scripts
from builtins import __import__
from _ast import Await
from cat import getCat
from discord.game import Game
from tkinter.constants import CURRENT
__import__
from googleapiclient.discovery import build

#import other python scripts
import key
from key import BotString, APIKey, SearchEngineID, BotID, DBotsToken


client = discord.Client()

#[---PRE-BOOT---]
print("Starting bot")

prefix = 's!'
adminPrefix = 's@'

#List of users who are allowed to use admin commands
adminList = ['211292458208854016','194525718300983296']

#List of all valid commands
commandList = ['cat','🐱','info','invite','greet','google','ping','poll','strawpoll','say','youtube','lmgtfy','LMGTFY','shutdown','changeGame','updateGuilds']


def google_search(query, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=query, cx=cse_id, **kwargs).execute()
    return res['items']

def youtube_search(api_key, **kwargs):
    service = build("youtube", "v3", developerKey=api_key)
    res = service.search().list(**kwargs).execute()
    return res['items']

def updateGuilds():
    serverCount = len(client.servers)
    requests.request(
        'POST',
                    
        'https://discordbots.org/api/bots/'+BotID+'/stats',
        headers={
            'authorization': DBotsToken
        },
        data = {
            'server_count': serverCount
        }
    )
    print("GUILD COUNT UPDATED ON discordbots.org")
    
#Bot comes online
@client.event
async def on_ready():
    print('Logging in as')
    print(client.user.name)
    print(client.user.id)
    
    #Set the bot's game to 's!help' on startup
    await client.change_presence(game=discord.Game(name='s!help'), status=None, afk=False,)
    serverCount = len(client.servers)
    updateGuilds()
    print("Running in", str(serverCount), "servers.")
    
    print('------------')
   
#[---COMMANDS---]
@client.event
async def on_message(message):
            
    if message.author != client.user: # Check to make sure the bot can't trigger its own commands
        
        #Command's contents are stored in commandContents
        if message.content.startswith(prefix) or message.content.startswith(prefix.upper()) or message.content.startswith(adminPrefix) or message.content.startswith(adminPrefix.upper()):
            commandString = message.content
            
            #String that stores the command (after prefix and before first space)
            #remove the commandContents
            command = commandString.split(' ', 1)[0]
            #remove the prefix
            command = command.split('!', 1)[-1]
            
            #String that stores the command's contents (after first space)
            commandContents = commandString.split(' ', 1)[-1]
            
            #Checks if command is valid or not
            if command in commandList:
                await client.add_reaction(message, '🦂')
            else:
                print(message.author, "ran an invalid command", command)
            
            
            
        #Command to inform users how to use the bot (Help command)
        if message.content.startswith(prefix+'help') or message.content.startswith(prefix.upper()+'help'):
            print("Sending", message.author, "help.")
            await client.send_message(message.author, '------------------------\n__**Commands**__\n\n'
                                      +'`cat`\nFinds a random image of a cat\n\n'
                                      +'`info`\nGet info related to the bot\n\n'
                                      +'`invite`\nInvite people to the current channel, or invite Scorpion Bot to your server.\n\n'
                                      +'`greet`\nSay hello to the bot\n\n'
                                      +'`google <Search contents>`\nGoogle search for something\n\n'
                                      +'`lmgtfy <Search contents>`\nGets a LMGTFY (Let me google that for you) link\n\n'
                                      +'`ping`\nPings the bot and checks to see if it is online\n\n'
                                      +'`poll <Poll contents>`\n Create a poll to let users vote\n\n'
                                      +'`reddit <Subreddit>`\nLink to a specific subreddit\n\n'
                                      +'`say <Message>`\nMake the bot say something\n\n'
                                      +'`youtube <Youtube search contents>`\n Search YouTube for something\n' # TODO: Add another line break if there were to be another command after youtube
                                      +'------------------------')
            await client.send_message(message.channel, message.author.mention+', sent you a DM.')
        
        #Command to respond with "Pong!" (For testing)
        elif message.content.startswith(prefix+'ping') or message.content.startswith(prefix.upper()+'ping'):
            await client.send_message(message.channel, 'Pong!')
            #Pring "Pong!" alongside the user's username and ID
            print("Pong!", message.author, message.author.id)
                       
        
        #Command to ping the bot (again)
        elif message.content.startswith(prefix+'greet'):
            await client.send_message(message.channel, 'Hello!')
            print("Hello!", message.author)
            
        #Command to generate an invite
        elif message.content.startswith(prefix+'invite') or message.content.startswith(prefix.upper()+'invite'):
            linkString = str(await client.create_invite(message.channel)) 
            await client.send_message(message.channel, '__Server Invite:__ <'+linkString+'>'
                                      +'\n__Bot Invite:__ <https://goo.gl/1SAbnr>')
            print("Created server invite at", message.author, "'s request")
        
        #Command to link to a specified subreddit
        elif message.content.startswith(prefix+'reddit ') or message.content.startswith(prefix.upper()+'reddit '):
            #remove spaces
            tempString = commandContents.replace(" ", "")
            await client.send_message(message.channel, 'https://www.reddit.com/r/' + tempString)
            print("Linked to subreddit", commandContents, "at", message.author, "'s request")
          
        #Command to give information about the bot  
        elif message.content.startswith(prefix+'info') or message.content.startswith(prefix.upper()+'info'):
            serverCount = len(client.servers)
            await client.send_message(message.author, 'Scorpion bot is a little bot made by Alstro20 and EmeraldOrbis. Check out the Github project at <https://github.com/Alstro20/ScorpionBot>'
                                      +'\nOfficial Discord server: http://discord.gg/vuT5xc8'
                                      +'\n__**Statistics**__:'
                                      +'\n\nScorpion is currently part of '+str(serverCount)+' servers.') #serverCount - 2 to compensate for our 2 private testing servrs.
            await client.send_message(message.channel, "Sent you a DM, " + message.author.mention)
            print("Info sent to", message.author) 
            
        #Command to make the bot say whatever
        elif message.content.startswith(prefix+'say ') or message.content.startswith(prefix.upper()+'say '):
            await client.delete_message(message)
            await client.send_message(message.channel, commandContents)
            print("Said - ", commandContents, " - at the request of", message.author)
            
        #Command to make the bot google search
        elif message.content.startswith(prefix+'google ') or message.content.startswith(prefix.upper()+'google '):
            resultsList = []
            print("Searched google for -", commandContents, "- at", message.author, "'s request")
            results = google_search(commandContents, APIKey, SearchEngineID, num = 3)
            for result in results:
                resultsList.append('**<' + result['link'] + '>** \n' + '```' + result['snippet'] + '```') #TODO: make this concatenation not so clunky
            await client.send_message(message.channel,  message.author.mention + ', Google search results for `' + commandContents + '`:\n'+'**1.**  '+resultsList[0]+'**2.**  '+resultsList[1]+'**3.**  '+resultsList[2])
            
        elif message.content.startswith(prefix+'youtube ') or message.content.startswith(prefix.upper()+'youtube '):
            resultsList = []
            results = youtube_search(APIKey, part = 'snippet', q = commandContents, type = 'video', maxResults=3)
            for result in results:
                resultsList.append('**<http://www.youtube.com/watch?v=' + result['id']['videoId'] + '>** \n' 
                                   + '```' + result['snippet']['title'] + '\n'
                                   + 'uploaded by ' + result['snippet']['channelTitle'] + '\n\n'
                                   + result['snippet']['description'] + '```\n')
            await client.send_message(message.channel, message.author.mention + ', Youtube search results for `' + commandContents + '`:\n'
                                     + '**1.** ' + resultsList[0]
                                     + '**2.** ' + resultsList[1]
                                     + '**3.** ' + resultsList[2])
            
        #Command to display a random cat
        elif message.content.startswith(prefix+'cat') or message.content.startswith(prefix.upper()+'cat') or message.content.startswith(prefix+'🐱'):
            print("Fetching cat image requested by", message.author)
            await client.send_typing(message.channel)
            randomCat = cat.getCat(directory=None, filename=None, format='jpg')
            await client.send_file(message.channel, randomCat)
            #reacts to the cat command with a 🐱 emoji
            await client.add_reaction(message, '🐱')
            #delete the cat picture after sending it
            os.remove(randomCat)
            print("Sent cat image at", message.author, "'s request. -", randomCat)
            
        #Command to give a link Let Me Google That For You (LMGTFY)
        elif message.content.startswith(prefix+'lmgtfy ') or message.content.startswith(prefix+'LMGTFY ') or message.content.startswith(prefix.upper()+'lmgtfy') or message.content.startswith(prefix.upper()+'LMGTFY'):
            print("Googled", commandContents, "for", message.author)
            #Replace the spaces in commandContents with +'s
            lmgtfyString = commandContents.replace(" ", "+")
            #Output the link
            await client.send_message(message.channel, message.author.mention+', Let me google that for you.\n<http://lmgtfy.com/?q='+lmgtfyString+'>')
            
        #Poll command
        elif message.content.startswith(prefix+'poll ') or message.content.startswith(prefix+'strawpoll ') or message.content.startswith(prefix.upper()+'poll') or message.content.startswith(prefix.upper()+'strawpoll'):
            await client.send_typing(message.channel)
            print("Poll created by", message.author, ":", commandContents)
            tempBotMessage = await client.send_message(message.channel, 'Poll by'+message.author.mention+':```'+commandContents+'```')
            #removes scorpion reaction
            await client.delete_message(message)
            #adds reactions to allow users to vote
            await client.add_reaction(tempBotMessage, '👍')
            await client.add_reaction(tempBotMessage, '👎')
            await client.add_reaction(tempBotMessage, '🤷')
            
            
        #[---ADMIN COMMANDS---]
        #Only users inside the adminList can use the following commands
        elif message.content.startswith(adminPrefix) or message.content.startswith(adminPrefix.upper()) and message.author.id in adminList:
                #Command to shut down the bot
            if message.content.startswith(adminPrefix+'shutdown') or message.content.startswith(adminPrefix.upper()+'shutdown'):
                await client.send_message(message.channel, 'Shutting down...')
                await client.change_presence(game=None,status=None,afk=False)
                time.sleep(2) # sleep for 2 seconds before shutdown, just to make sure status changed correctly
                await client.logout()
                print("Shutting down at", message.author, "'s request") 
                
                
            #Change the bot's current game with an admin command    
            elif message.content.startswith(adminPrefix+'changeGame ') or message.content.startswith(adminPrefix.upper()+'changeGame '):
                #String to store the bot's current game
                currentGame = commandContents
                print("Changing current game to", commandContents, "at the admin request of", message.author)
                await client.change_presence(game=discord.Game(name=currentGame), status=None, afk=False,)
                client.delete_message(message) #NOT SURE WHY NOT WORKING
                
            elif message.content.startswith(adminPrefix+'updateGuilds'):
                updateGuilds()
                print("Updating Guilds at", message.author, "'s request")

                
                
            #User failed to authenticate (PUT ALL ADMIN COMMANDS BEFORE THIS)
            elif message.author.id not in adminList:
                    await client.send_message(message.channel, 'Error: You are not a bot admin, '+message.author.mention)
                    print(message.author, "tried to shutdown the bot but it not admin")
            
        
client.run(BotString)
