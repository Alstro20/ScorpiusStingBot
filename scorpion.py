import discord
import asyncio
from discord.enums import Status
import time

client = discord.Client()

prefix = 's!'


async def reddit(message):
    await client.send_message(message.channel, 'https://www.reddit.com/r/'+ message.content[(len(prefix)+7):])

#Bot comes online
@client.event
async def on_ready():
    print('Logging in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
   
#Bot checks for messages being sent
@client.event
async def on_message(message):
    #Ping
    if message.content.startswith(prefix+'ping'):
        await client.send_message(message.channel, 'Pong!')
        print("Pong!")
        
    #Command to shut down the bot
    if message.content.startswith(prefix+'shutdown'):
        await client.send_message(message.channel, 'Shutting down')
        await client.change_presence(game=None,status=None,afk=False)
        #sleep for 2 seconds before shutdown, just to make sure status changed correctly
        time.sleep(2)
        await client.close()
        print("Shutdown") 
    
    #Command to ping the bot (again)
    if message.content.startswith(prefix+'greet'):
        await client.send_message(message.channel, 'Hello!')
        print("Hello!")        
        
    #Command to DM a user that requests it
    if message.content.startswith(prefix+'dm'):
        await client.send_message(message.author, 'Slidin into the DMs ;)')
        await client.send_message(message.channel, 'Sent you a message')
        print("sent a message")
    #command to link to a specified subreddit
    elif message.content.startswith(prefix+'reddit'):
        await reddit(message)
client.run('MzQyMzc5OTg5MDk1Njc3OTUz.DGOxug.wbSojJmHCDlq6Z0t70za4ZjWyzA')
