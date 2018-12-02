import discord
from discord.ext import commands

class Commands():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["t"], description='Temporary command KEK')
    async def test(self, ctx):
        await ctx.send("Test")

    @commands.command(aliases=["attack"], description='Have magikarp attack a user!')
    async def splash(self, ctx, *, target: discord.User):
        embed = discord.Embed(title='Magikarp used splash against '+target.name, colour=ctx.author.colour)
        embed.set_author(icon_url=self.bot.user.avatar_url, name=str(self.bot.user.name))
        await ctx.send(content=None, embed=embed)


def setup(bot):
    bot.add_cog(Commands(bot))