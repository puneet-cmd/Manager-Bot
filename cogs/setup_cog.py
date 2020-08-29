import os
import json

import discord 
from discord import Embed
from discord.ext import commands

class Setup(commands.Cog): 
    
    def __init__(self, bot): 
        self.bot = bot 
        self.bot_name = bot.user.display_name
        self.bot_url = bot.user.avatar_url
        self.embed_colour = discord.Color.from_rgb(255, 255, 0)
        
    async def create_team_vc(self, guild, number, elite_manager = True): 
        basic_perms = discord.PermissionOverwrite(
            view_channel = True, 
            connect = True, 
            use_voice_activation = True, 
            speak = True
        )
        
        no_perms = discord.PermissionOverwrite(
            view_channel = True, 
            connect = False, 
            use_voice_activation = True, 
            speak = True
        )
        
        elite_perms = discord.PermissionOverwrite(
            view_channel = True, 
            connect = True, 
            use_voice_activation = True, 
            speak = True, 
            move_members = True
        )
        
        if elite_manager: 
            manager_role = await guild.create_role(name = "Tournament Manager")
        
        for i in range(1, number + 1): 
            role = await guild.create_role(name = f"Team {i}")
            await guild.create_voice_channel(name = f"Team {i}", 
                overwrites = {
                    guild.default_role : no_perms, 
                    role : basic_perms, 
                    manager_role : elite_perms
                })
            
        
        
    @commands.command(usage = "auto_setup", aliases = ["auto-setup"])
    async def auto_setup(self, cont): 
        
        """
        This command will automatically setup the bot.
        """
        
        # Questions 1 
        """
        -------------------------------
        1) how many teams are their ? 
        ans - integer paramatere
        ---------------------------------
        """
        
        embed = Embed(title = "Steps 1/4", 
                colour = self.embed_colour, 
                description = "Type the total number of teams participating :-")
                
        await cont.channel.send(embed = embed)
                
        def check(m): 
            if m.author == cont.author and m.channel == cont.channel: 
                try : 
                    number = int(m.content.strip())
                except : 
                    return False 
                else : 
                    if number >= 0: 
                        return True 
                    else : 
                        print("Please enter a valid poitive integer.")
                        return False 
                
        msg = await self.bot.wait_for("message", check = check, timeout = 60)
        team_no = int(msg.content.strip())
        
        await cont.channel.send(f"Creating {team_no} voice channel/channels")
        
        await sef.create_team_vc(cont.guild, team_no)
        
        ## QUESTION:  2
        
def setup(bot): 
    bot.add_cog(Setup(bot))
            
            