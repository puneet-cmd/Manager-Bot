import os
import json

import discord 
from discord import Embed
from discord.ext import commands

current_dir = os.path.dirname(__file__)
parent_dir = os.path.split(current_dir)[0]

data_dir = os.path.join(parent_dir, "data")

class Config(commands.Cog): 
    
    def __init__(self, bot): 
        self.bot = bot 
        self.bot_name = bot.user.display_name
        self.bot_url = bot.user.avatar_url
        self.embed_colour = discord.Color.from_rgb(255, 255, 0)
        
    def get_prefix(self, id): 
        """
            returns prefix for the server id provided
            -----------------------------------------
            :param id: server id 
        """
        
        with open(os.path.join(data_dir, "config.json"), "r") as file: 
            data = json.load(file)
            default_prefix = data.get("default_prefix")
            
        with open(os.path.join(data_dir, "prefixes.json"), "r") as file: 
            data = json.load(file)
            prefix = data.get(str(id), default_prefix)
        
        return prefix
        
    def set_new_prefix(self, id, new_prefix): 
        """
            sets the new prefix for the server id provided
            ----------------------------------------------
            :param id: server id 
            :param new_prefix: new prefix to set
        """
        
        with open(os.path.join(data_dir, "prefixes.json"), "r") as file: 
            data = json.load(file)
            data[id] = new_prefix
            
        with open(os.path.join(data_dir, "prefixes.json"), "w") as file: 
            json.dump(data, file, indent = 2)
        
    @commands.command(usage = "prefix your_new_prefix_here")
    async def prefix(self, cont, new_prefix = None): 
        """
            Sets a new custom prefix for the server.
            ------------
            Note that :- 
                It will return current prefix if new_prefix is not provided.
        """
        
        if new_prefix is None: 
            embed = Embed(title = "Prefix", colour = self.embed_colour, 
                description = f"Prefix for this server is `{self.get_prefix(cont.guild.id)}`")
            
            await cont.channel.send(embed = embed)
            
        elif len(new_prefix) <= 5: 
            self.set_new_prefix(str(cont.guild.id), new_prefix)
            embed = Embed(title = "Success", colour = self.embed_colour, 
                description = f"Prefix for this server is now `{self.get_prefix(cont.guild.id)}`")
            
            await cont.channel.send(embed = embed)

def setup(bot): 
    bot.add_cog(Config(bot))
            
            