import discord, datetime, asyncio
import responses, secrets
from discord import EventStatus
from discord.ext import commands
from secrets import TOKEN, channel_id

description = '''Dot Matrix helps Team Ludicrous Speed  .'''

intents = discord.Intents.default()
intents.message_content = True
intents.guild_scheduled_events = True
client = commands.Bot(command_prefix='!', description=description, intents=intents)

def run_discord_bot():
    @client.event
    async def on_ready():
        print(f'{client.user} is now online')
        await schedule_daily_message(client)

    client.run(TOKEN)

async def schedule_daily_message(client):
    # wait and send a message
    now = datetime.datetime.now()
    #then = now+datetime.timedelta(days=1)
    then = now.replace(hour=12, minute=0)
    wait_time = (then - now).total_seconds()
    #sends the message to the first channel in all guilds
    await asyncio.sleep(wait_time)
    for guild in client.guilds:
        channel = guild.text_channels[0]
        print(channel)
        await channel.send("Good afternoon everyone don't forget you're all cracked")

async def send_message(message, user_message, is_private):
    try:
        response = responses.get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)


@client.event
async def on_scheduled_event_create(event):
    #Start Events at the scheduled start time
    channel = event.channel
    name = str(event.name)
    start_time = event.start_time
    now = datetime.datetime.now(datetime.timezone.utc)
    wait_time = (start_time - now).total_seconds()
    print(f'{name} is scheduled in {wait_time} seconds')
    await asyncio.sleep(wait_time)
    await event.edit(status=EventStatus.active, channel=channel)

@client.command()
async def info(ctx):
    """Gives Users The Bot Commands"""
    await interaction.response.send_message("Text", ephemeral=True)
