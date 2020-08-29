import os
import json
import asyncio

import discord
from discord import Embed
from discord.ext import commands
from discord.ext.tasks import loop
from discord.ext.commands import when_mentioned_or

with open('data/config.json', 'r') as file:
    """
        Retrieving data from config (json file)
    """
    data = json.load(file)
    token = data.get("token")
    default_prefix = data.get("default_prefix")
    
def get_prefix(bot, message): 
    
    if message.guild is not None: 
        
        id = message.guild.id
        
        with open('data/prefixes.json', "r") as file: 
            data = json.load(file)
            prefix = data.get(str(id), default_prefix)
            
        return when_mentioned_or(prefix)(bot, message)
    
    else : 
        pass

client = commands.Bot(command_prefix = get_prefix, case_insensitive = True)
client.remove_command("help")

class Main(commands.Cog):

    def __init__(self, bot : discord.Client):
        """
            Initializing our Main class with bot
        """
        self.bot = bot

    @loop(seconds = 5)
    async def change_presence_loop(self):
        """
            A background loop handler which uses commands.ext.tasks.loop couroutine.
            ------------------------------------------------------------------------
            status :
                type - Dictionary
                keys - Keys representing status type (from game, music, stream or movie)
                values - representing activity name.

            seconds :
                type - int
                Change this to change the iteration time between two sucessive status change.
        """

        servers = len(client.guilds)
        members = sum([s.member_count for s in client.guilds])
        seconds = 5

        status = {
            "game": f"in {servers} servers",
            "music": f"@{self.bot.user.name} help",
            "movie": f"{members} members",
            # "stream": "Tournaments"
        }

        for key, value in zip(status.keys(), status.values()):
            if key == "game":
                await client.change_presence(
                    activity = discord.Game(name = value)
                    )

            elif key == "music":
                await client.change_presence(
                    activity = discord.Activity(type = discord.ActivityType.listening,
                        name = value)
                )

            elif key == "movie":
                await client.change_presence(
                    activity = discord.Activity(type = discord.ActivityType.watching,
                        name = value)
                )

            if key == "stream":
                await client.change_presence(
                    activity = discord.Streaming(name = value,
                    url = "https://www.twitch.tv/managertv")
                    )

            else:
                pass

            await asyncio.sleep(seconds)

    @commands.Cog.listener()
    async def on_ready(self):
        """
            Function that is called when bot is ready.
            -------------------------------------------------------------
            Here can do things which have to setup after bot is logged in.
        """

        print(f"Logged in as {self.bot.user}")

        #Loading Extensions
        print("\n\nLoading Extensions")
        Extensions = [
            'cogs.help_cogs',
            'cogs.info_cogs',
            'cogs.errors', 
            'cogs.config_cogs', 
            'cogs.setup_cog'
        ]

        for extension in Extensions:
            self.bot.load_extension(extension)
            print(f"Loaded {extension}")

        print("\n\nBOT IS READY")

        #Changing presence

        change_presence_loop = self.change_presence_loop
        await change_presence_loop.start()

#Running our BOT
if __name__ == "__main__":
    client.add_cog(Main(client))

    print("Logging into the bot")
    client.run(token)
