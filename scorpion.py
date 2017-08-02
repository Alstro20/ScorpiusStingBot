import discord
import asyncio
from discord.enums import Status
import time
from builtins import int

client = discord.Client()

#Runs before bot starts
print("Starting bot")

prefix = 's!'

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
    #Command to respond with "Pong!" (For testing)
    if message.content.startswith(prefix+'ping'):
        await client.send_message(message.channel, 'Pong!')
        print("Pong!")
        
    #Command to shut down the bot
    if message.content.startswith(prefix+'shutdown'):
        await client.send_message(message.channel, 'Shutting down')
        await client.change_presence(game=None,status=None,afk=False)
        #sleep for 2 seconds before shutdown, just to make sure status changed correctly
        time.sleep(2)
        await client.logout()
        print("Shutdown") 
    
    #Command to ping the bot (again)
    if message.content.startswith(prefix+'greet'):
        await client.send_message(message.channel, 'Hello!')
        print("Hello!")        
        
    #Command to DM a user that requests it
    if message.content.startswith(prefix+'dm'):
        await client.send_message(message.author, 'Slidin into the DMs ;)')
        print("sent a message")
        
    #Command to generate an invite
    if message.content.startswith(prefix+'invite'):
        await client.send_message(message.channel, await client.create_invite(message.channel))
        print("Created server invite")

		
client.run('MzQyMzc5OTg5MDk1Njc3OTUz.DGOxug.wbSojJmHCDlq6Z0t70za4ZjWyzA')
