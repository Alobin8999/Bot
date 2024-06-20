import asyncio
import discord
import os
from discord.ext import commands

TOKEN = "MTAxNzg5MTE0ODUzNjIzODE0MA.GSZgnt.8h2cv6ATD4QTaJtVn9EbAhNld4YGitZd-h3BRU"
PREFIX = "!"

intents = discord.Intents().all()
client = commands.Bot(command_prefix=PREFIX, intents=intents)

@client.event
async def on_ready():
    print("Бот запущен")

@client.command(name='очистить')
async def clear(ctx, amount=None):
    await ctx.channel.purge(limit=int(amount)+1)

'''async def load_extensions():
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")'''

async def main():
    async with client:
        #await load_extensions()
        await client.start(TOKEN)

asyncio.run(main())