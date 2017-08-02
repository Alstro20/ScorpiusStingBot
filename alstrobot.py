import discord
import asyncio
from discord.enums import Status

client = discord.Client()

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
    #Ping
    if message.content.startswith(prefix+'ping'):
        await client.send_message(message.channel, 'Pong!')
        print("Pong!")
        
    #Command to shut down the bot
    if message.content.startswith(prefix+'shutdown'):
        await client.send_message(message.channel, 'Shutting down')
        await client.change_status(None, Status.invisible)
        await client.close()
        print("Shutdown")
    

client.run('MzQyMzM0NzE2MTM5MTQzMTY5.DGOHmA.fHEu372uduE5hwGZ7vjFzS0BmJQ')
