import discord
import asyncio
import time
#allows import of other python scripts
from builtins import __import__
__import__

#import other python scripts
import key
from key import BotString



client = discord.Client()

#[---PRE-BOOT---]
print("Starting bot")
print("DEV VERSION MIGHT NOT BE STABLE")

prefix = 's!'

#Bot comes online
@client.event
async def on_ready():
    print('Logging in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
   
#[---COMMANDS---]
@client.event
async def on_message(message):
    #Command's contents are stored in commandContents
    if message.content.startswith(prefix):
        commandString = message.content
        commandContents = commandString.split(' ', 1)[-1]
        
    
    #Command to respond with "Pong!" (For testing)
    if message.content.startswith(prefix+'ping'):
        await client.send_message(message.channel, 'Pong!')
        print("Pong!")
        
    #Command to shut down the bot
    elif message.content.startswith(prefix+'shutdown'):
        await client.send_message(message.channel, 'Shutting down')
        await client.change_presence(game=None,status=None,afk=False)
        #sleep for 2 seconds before shutdown, just to make sure status changed correctly
        time.sleep(2)
        await client.logout()
        print("Shutdown") 
    
    #Command to ping the bot (again)
    elif message.content.startswith(prefix+'greet'):
        await client.send_message(message.channel, 'Hello!')
        print("Hello!")        
        
    #Command to DM a user that requests it
    elif message.content.startswith(prefix+'dm'):
        await client.send_message(message.author, 'Slidin into the DMs ;)')
        print("sent a message")
        
    #Command to generate an invite
    elif message.content.startswith(prefix+'invite'):
        await client.send_message(message.channel, await client.create_invite(message.channel))
        print("Created server invite")
    
    #Command to link to a specified subreddit
    elif message.content.startswith(prefix+'reddit'):
        await client.send_message(message.channel, 'https://www.reddit.com/r/'+commandContents)
        print("Reddit")
      
    #Command to give information about the bot  
    elif message.content.startswith(prefix+'info'):
        await client.send_message(message.author, "Scorpion bot is a little bot made by Alstro20 and EmeraldOrbis. Check out the Github project at https://github.com/Alstro20/ScorpiusStingBot")
        await client.send_message(message.channel, message.author, "Send you a DM")
        print("Info sent to", message.author) 
        
    #Command to make the bot say whatever
    elif message.content.startswith(prefix+'say'):
        await client.delete_message(message)
        await client.send_message(message.channel, commandContents)
        print("Said - ", commandContents, " - at the request of", message.author)
        
        
    
    #Lets user know if script is unknown. Put all commands before this.
    elif message.content.startswith(prefix):
        await client.send_message(message.channel, 'Invalid Command')  

        
client.run(BotString)
