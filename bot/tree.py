import discord, datetime, asyncio
import responses
from discord import (EventStatus, app_commands)
from discord.ext import commands

description = '''Dot Matrix helps Team Ludicrous Speed  .'''

TOKEN = 'MTA2OTcyNDkwNzQ1NTM5Mzk5NA.Gm80_D.RwZwCteipKk60PUe6L6otMoIPbGB4bNt7vZgT8'
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

def run_discord_bot():
    @client.event
    async def on_ready():
        print(f'{client.user} is now online')
        await schedule_daily_message(client)

    @client.event
    async def on_ready():
        await tree.sync(guild=)
        print("Ready!")

    client.run(TOKEN)

async def schedule_daily_message(client):
    # wait and send a message
    now = datetime.datetime.now()
    then = now+datetime.timedelta(days=1)
    then.replace(hour=9, minute=0)
    wait_time = (then - now).total_seconds()
    await asyncio.sleep(wait_time)

    channel = client.get_channel(1065826052519252020)
    await channel.send("Good morning everyone don't forget you're all cracked")

async def send_message(message, user_message, is_private):
    try:
        response = responses.get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)


@client.event
async def on_scheduled_event_create(event):
    channel = event.channel
    name = str(event.name)
    start_time = event.start_time
    now = datetime.datetime.now(datetime.timezone.utc)
    wait_time = (start_time - now).total_seconds()
    print(f'{name} is scheduled in {wait_time} seconds')
    await asyncio.sleep(wait_time)
    await event.edit(status=EventStatus.active, channel=channel)

@tree.command(name = "commandname", description = "My first application Command", guild=discord.Object(id=1065826051940417536)) #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def first_command(interaction):
    await interaction.response.send_message("Hello!")
