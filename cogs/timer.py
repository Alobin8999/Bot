import discord
from discord.ext import tasks, commands
from datetime import date, datetime
import sqlite3

channel_id = 1204484985084452926

database = sqlite3.connect("planner.sqlite")
cursor = database.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS timer(message_id INT, set_time INT, message TEXT, sender_id INT)""")

class time_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.printer.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print("HomaTimer запущен")

    @tasks.loop(seconds=1)
    async def printer(self):
        cursor.execute(f"SELECT * FROM timer")
        result = cursor.fetchall()
        for element in result:
            print(element[1])
            if int(element[1]) != 0:
                cursor.execute(f"UPDATE timer SET set_time = {int(element[1]) - 1} WHERE message_id = {element[0]}")
                database.commit()
            elif int(element[1]) <= 0:
                for guild in self.bot.guilds:
                    for member in guild.members:
                        if member.id == int(element[3]):
                            await self.bot.get_channel(channel_id).send(f"Напоминание для {member.mention}:\n{element[2]}")
                cursor.execute(f"DELETE FROM timer WHERE message_id IN(SELECT message_id FROM timer ORDER BY set_time LIMIT 1)")
                database.commit()

    @commands.command(name="добавить")
    async def add_timer(self, ctx, set_time, messagestr):
        message_id = 0

        ftr = [3600, 60, 1]
        set_time = sum([a * b for a, b in zip(ftr, map(int, set_time.split(':')))])

        cursor.execute(f"SELECT * FROM timer")
        result = cursor.fetchall()
        for get_max_id in result:
            if get_max_id[0] > message_id:
                message_id = get_max_id[0]
        sender_id = ctx.message.author.id
        cursor.execute(f"INSERT INTO timer(message_id, set_time, message, sender_id) VALUES ({message_id + 1}, '{set_time}', '{messagestr}', '{sender_id}')")
        database.commit()
        seted_time = datetime.utcfromtimestamp(set_time).strftime('%H:%M:%S')
        await ctx.send('Таймер, содержащий "' + messagestr + '", сработает через ' + str(seted_time))

    @commands.command(name="список")
    async def check_timer(self, ctx):
        cursor.execute(f"SELECT * FROM timer")
        elements = cursor.fetchall()

        mbed = discord.Embed(title="Список таймера: ", color=discord.Color.from_rgb(139,0,0))
        index = 1
        for element in elements:
            passed_time = datetime.utcfromtimestamp(int(element[1])).strftime('%H:%M:%S')
            for guild in self.bot.guilds:
                for member in guild.members:
                    if member.id == int(element[3]):
                        sender = member.guild.get_member(element[3]).display_name
            mbed.add_field(name=f"Напоминание через {passed_time} для {sender}",value=f"{element[2]}",inline=False)
            index += 1
            if index == elements and index <= 10:
                break
        await ctx.send(embed=mbed)

    @commands.command(name="удалить")
    async def del_all(self, ctx):
        cursor.execute(f"DELETE FROM timer")
        database.commit()
        await ctx.send('Таймер удален')

async def setup(bot):
    await bot.add_cog(time_commands(bot))