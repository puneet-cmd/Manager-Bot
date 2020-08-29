import discord
import asyncio
import json
import os

from asyncio import TimeoutError
from discord import Embed
from discord.ext import commands
from discord.ext.commands.errors import BadArgument, MissingRequiredArgument, CommandNotFound

class Errors(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.embed_colour = discord.Colour.from_rgb(250, 0, 0)


    @commands.Cog.listener()
    async def on_command_error(self, cont, error):

        if isinstance(error, BadArgument):
            embed = Embed(colour = self.embed_colour, title="**Error**", description = f"**­Please provide correct argument, \nfor more info use {cont.prefix}help**")
            await cont.send(embed=embed)

        elif isinstance(error, MissingRequiredArgument):
            embed = Embed(colour = self.embed_colour, title="**Error**", description = f"**­Please provide required argument, \nfor more info use {cont.prefix}help**")
            await cont.send(embed=embed)

        elif isinstance(error, CommandNotFound):
            embed = Embed(colour = self.embed_colour, title="**Error**", description = f"**No such command found, \nfor list of commands use {cont.prefix}help**")
            await cont.send(embed=embed)
            
        elif isinstance(error, TimeoutError): 
            embed = Embed(colour = self.embed_colour, title="**Error**", description = f"**Canceliing the command. \nUser didn't answer in time.**")
            await cont.send(embed=embed)

        else:
            error_str = str(error)
            error = getattr(error, 'original', error)
            print(f"Error:: {error_str}")

def setup(bot):
    bot.add_cog(Errors(bot))
