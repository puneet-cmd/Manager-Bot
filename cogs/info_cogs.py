import discord
import json
import os

from discord import Embed
from discord.ext import commands

class Info(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.embed_colour = discord.Colour.from_rgb(234, 255, 0)
        self.bot_name = bot.user.display_name
        self.bot_url = bot.user.avatar_url

    @commands.command(usage = "status")
    async def status(self, cont):
        """
            Displays status of the bot.
        """
        embed = Embed(colour = self.embed_colour, description = "­\n")
        embed.set_author(name = self.bot_name+" Status", icon_url = self.bot_url)

        name_value = {
            "Ping": f"{round(self.bot.latency * 1000)} ms",
            "Server Count": f"{len(self.bot.guilds)}",
            "Member Count": f"{sum([s.member_count for s in self.bot.guilds])}"
        }

        for name, value in zip(name_value.keys(), name_value.values()):
            embed.add_field(name = name, value = value, inline = False)

        await cont.channel.send(embed = embed)

def setup(bot):
    bot.add_cog(Info(bot))
