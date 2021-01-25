import discord
from discord.ext import commands
from discord.voice_client import VoiceClient
import asyncio
import os
import youtube_dl
from discord.utils import get


intents=intents=discord.Intents.all()
prefix = "?"
client = commands.Bot(command_prefix='.', intents = intents)

#sets the status lf the bot
@client.event
async def on_ready():
    await client.change_presence(
        activity=discord.Game(name="a song"))

@client.command()
async def credits(ctx):
    await ctx.send('Made by Louay Ahmad')

#sends a private message to new members
@client.event
async def on_member_join(member):
    await member.send('Welcome to the Discord! Please be respectful, toxic behavior will not be tollerated. Members will have the ability to kick or ban those who disobey the rules. Have fun!')

#if user says hello, the bot will respond
@client.event
async def on_message(message):
    if message.content == "hello":
        await message.channel.send("Hello and welcome!")
    await client.process_commands(message)


#povides the user's ping
@client.command()
async def ping(ctx):
    await ctx.send(f'Latency: {round(client.latency * 1000)} ms')


#prints the message the user specified the bot to print
@client.command()
async def print(ctx, arg):
    await ctx.channel.send(arg)


#clears discord chat, 1000 lines of messages
@client.command()
async def clear(ctx, number=1000):
    await ctx.channel.purge(limit=number)


#kicks a member in the discord
@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} was kicked')


#bans a member in the discord
@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} was banned')


#loops through all of the banned users and unbans the user that was specified
@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name,
                                               member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned{user.mention}')
            return

#Music feature for bot code begins:

#allows bot to join one of the active voice channels
@client.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await voice.disconnect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"Connected")

    await ctx.send(f"Connected")

#disconnects bot from the active voice channel
@client.command(pass_context=True)
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"Disconnected")
        await ctx.send(f"Disconnected")
    else:
        print("Not in voice channel")
        await ctx.send("Not in voice channel")

#plays a song in the voice chat using youtube_dl and ffmpeg after a member inputs a youtube url
@client.command()
async def play(ctx, url : str):

  song_there = os.path.isfile("song.mp3")

  try:
    if song_there:
      os.remove("song.mp3")
  except PermissionError:
    print("Trying to delete song file, but it's being played")
    await ctx.send("There is music playing...")
    return

  await ctx.send("Music will begin shortly...")

  channel = ctx.message.author.voice.channel
  await channel.connect()
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

  ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    print("Downloading audio now\n")
    ydl.download([url])

  for file in os.listdir("./"):
    if file.endswith(".mp3"):
      name = file
      print(f"Renamed File: {file}\n")
      os.rename(file, "song.mp3")
  
  voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print("Song done!"))
  voice.source = discord.PCMVolumeTransformer(voice.source)
  voice.source.volume = 0.07

  nname = name.rsplit("-", 2)
  await ctx.send(f"Playing: {nname}")
  print("playing\n")

    
client.run('ODAyMzIzMDA3ODE3MTIxODYy.YAtjhw.jL5wq6-ZdBv4G8i0rTNmp22weDE')

