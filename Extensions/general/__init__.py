import discord
from discord.ext import commands

from .paginator import HelpPaginator, CannotPaginate

class General():
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_command(commands.Command("help", self._help))

    async def _help(self, ctx, *, command: str = None):
        """Shows help about a command or the bot"""

        if command is None:
            p = await HelpPaginator.from_bot(ctx)
        else:
            entity = self.bot.get_cog(command) or self.bot.get_command(command)

            if entity is None:
                clean = command.replace('@', '@\u200b')
                return await ctx.send(f'Command or category "{clean}" not found.')
            elif isinstance(entity, commands.Command):
                p = await HelpPaginator.from_command(ctx, entity)
            else:
                p = await HelpPaginator.from_cog(ctx, entity)

        await p.paginate()

def setup(bot):
    bot.remove_command("help")
    bot.add_cog(General(bot))

def teardown(bot):
    bot.add_command(commands.Command("help", commands.bot._default_help_command))
