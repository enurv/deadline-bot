import discord
from discord.ext import tasks, commands
import asyncio
import datetime
from variables import token, channel_id
from db import list_deadlines, connect_to_database, new_deadline, remind_deadline, warn_deadline

def main():
    client = discord.Client()

    @client.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(client))
        check_the_date.start()

    @client.event
    async def on_message(message):       
        if message.author == client.user:
            return

        if message.content.startswith('$list'):
            connection = connect_to_database()
            deadlines = list_deadlines(connection)
            formatted_message = ""
            for i in range(len(deadlines)):
                formatted_message = formatted_message + deadlines[i] + "\n"
            await message.channel.send(formatted_message)

        if message.content.startswith('$new-deadline'):
            connection = connect_to_database()
            message_formatted = message.content.split()[1]
            new_deadline_request = message_formatted.split(',')
            if len(new_deadline_request) < 2:
                return
            elif len(new_deadline_request) == 2:
                new_deadline(connection, new_deadline_request[0], new_deadline_request[1], "")
            elif len(new_deadline_request) == 3:
                new_deadline(connection, new_deadline_request[0], new_deadline_request[1], new_deadline_request[2])
            elif len(new_deadline_request) > 3:
                return
            await message.channel.send("New deadline is added. Thanks!")

    @tasks.loop(hours = 24)
    async def check_the_date():
        announcement_channel = client.get_channel(channel_id)
        connection = connect_to_database()
        reminders = remind_deadline(connection)
        message = ""
        if reminders:
            message += "Less then 1 week before the below deadlines!"
            for i in range(len(reminders)):
                message += "\n" + str(reminders[i])
        connection1 = connect_to_database()
        warnings = warn_deadline(connection1)
        if warnings:
            message += "\nToday is the last day for belo!! Don't forget to submit your application-!"
            for i in range(len(warnings)):
                message += "\n" + str(warnings[i]) 
        if message:
            await announcement_channel.send(message)

    @check_the_date.before_loop
    async def before_check_the_date():
        for _ in range(60*60*24):  # loop the hole day
            if datetime.datetime.now().hour == 22:  # 24 hour format
                print('It is time')
                return
            await asyncio.sleep(1)# wait a second before looping again. You can make it more 

    client.run(token)

main()