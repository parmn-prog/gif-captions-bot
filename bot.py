import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import re
import random

paths = ["lb.png", "lang.jpg"]

BANNED_WORDS: str

with open("en", "r") as file:
    BANNED_WORDS = file.read().strip()

PATTERN = re.compile(
    r"\b(" + "|".join(map(re.escape, BANNED_WORDS)) + r")\b",
    re.IGNORECASE
)

load_dotenv()


intents = discord.Intents.default()
intents.message_content = True
intents.auto_moderation = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_automod_action(execution):
    print("executed")
    await execution.channel.send(file=discord.File(random.choice(paths)))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    for line in BANNED_WORDS.splitlines():
        if (line + " " in message.content.lower() and line[0] == message.content[0])\
            or (" " + line in message.content.lower() and line[-1] == message.content[-1]) or\
        " " + line + " " in message.content.lower() or line == message.content.lower():
            print("BAD WORD")
            await message.channel.send(content=f"{message.author.mention}",file=discord.File(random.choice(paths)))
            break


token = os.getenv("BOT_TOKEN")
if token is None:
    raise RuntimeError("Token is not set")


client.run(token)
