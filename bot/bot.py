import discord, datetime, asyncio, sqlite3
import responses, secrets
from discord import EventStatus
from discord.ext import commands
from secrets import TOKEN, channel_id

description = '''Dot Matrix helps Team Ludicrous Speed .'''

intents = discord.Intents.default()
intents.message_content = True
intents.guild_scheduled_events = True
intents.members = True
client = commands.Bot(command_prefix='!', description=description, intents=intents)

#db
client.db = sqlite3.connect('sd.db')
cur = client.db.cursor()
#Create Table
cur.execute('''
CREATE TABLE IF NOT EXISTS sd_jar
    (id integer PRIMARY KEY,
    username text,
    sd_count integer
    )
''')

def run_discord_bot():
    @client.event
    async def on_ready():
        print(f'{client.user} is now online')
        await schedule_daily_message(client)

    client.run(TOKEN)

async def schedule_daily_message(client):
    # wait and send a message
    now = datetime.datetime.now()
    then = now+datetime.timedelta(days=1)
    then.replace(hour=12, minute=0)
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
async def test(ctx, arg):
    await ctx.send(arg)

@client.command()
async def jar(ctx, arg: str = commands.parameter(description="Use !jar and tag someone with @ to track their self-deprecation.")):
    guild = ctx.guild
    arg_n = ""
    for element in range(2, len(arg)):
        if arg[element] != ">":
            arg_n += arg[element]
    async for member in guild.fetch_members():
        #print(member.name)
        n = str(member.id)
        if n == arg_n:
            cur.execute('''
        INSERT OR IGNORE INTO sd_jar (id, username, sd_count)
            VALUES (?, ?, ?)
        ''', [member.id, str(member.name), 0])
            client.db.commit()
            cur.execute('''
        UPDATE sd_jar SET sd_count = sd_count + 1 WHERE id = ?
        ''', [member.id])
            client.db.commit()
            cur.execute("SELECT sd_count FROM sd_jar WHERE id = ?", [member.id])
            data = cur.fetchone()
            print(member.name + " has self deprecated themselves " + str(data[0]) + " times!")
            if data[0] == 1:
                await ctx.send(member.name + " has self-deprecated themselves for the first time! Throw a dollar in the jar. Be careful, it adds up quickly...")
                return
            await ctx.send(member.name + " has self-deprecated themselves " + str(data[0]) + " times! Throw another dollar in the self-deprecation jar!")
            return
        #for row in cur.execute('SELECT * FROM sd_jar'):
        #    print(row)
    await ctx.send("User could not be found. Check the tag you used and try again.")

@client.command()
async def ok(ctx):
    n = ctx.guild.id
    await ctx.send(n)
