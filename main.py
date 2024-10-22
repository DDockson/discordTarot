import discord
from discord.ext import commands
import json
import asyncio
import os

with open("token.json", 'r', encoding='utf-8') as f:
    config = json.load(f)
token = config["token"]

intents = discord.Intents.default()
intents.message_content = False

bot = commands.Bot(command_prefix="!",intents = intents)

async def load():
    for filename in os.listdir("./commands"):
        if filename.endswith("py"):
            await bot.load_extension(f"commands.{filename[:-3]}")

@bot.event
async def on_ready():
    print('Ready!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="타로"))
    await bot.tree.sync()

asyncio.run(load())

bot.run(token)