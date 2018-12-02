import traceback
import sys
from discord.ext import commands
import discord

from utils.helpers import copy_func

class CommandErrorHandler():
    def __init__(self, bot):
        self.bot = bot
        self.initialize_cog()

    async def _on_command_error(self, ctx, error):
        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send(':x: This command cannot be used in private messages.', delete_after=10)
        elif isinstance(error, commands.DisabledCommand):
            await ctx.message.add_reaction('🚫')
            await ctx.send("Sorry! This command is disabled and cannot be used... The fix is coming soon.", delete_after=10)
        elif isinstance(error, commands.CheckFailure) or isinstance(error, commands.NotOwner):
            await ctx.message.add_reaction('🚫')
            await ctx.send("You don't have permissions to use this command.", delete_after=10)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"The `{error.param.name}` is a required argument and is missing...")
        elif isinstance(error, commands.BadArgument):
            await ctx.send(f"Bad argument has been passed to the command `{ctx.command.name}`...")
        elif isinstance(error, commands.CommandOnCooldown):
            minutes, seconds = divmod(error.retry_after, 60)
            await ctx.send(embed=discord.Embed(color=0x99AAB5, description=f':clock12: This command is on cooldown. Please wait {int(round(minutes))}' \
            f' minutes and {int(round(seconds))} seconds.'), \
            delete_after=10)
        elif isinstance(error, commands.CommandInvokeError) and hasattr(error, 'original'):
            print('In {}:'.format(ctx.command.qualified_name), file=sys.stderr)
            traceback.print_tb(error.original.__traceback__)
            print('{0}: {1}'.format(error.original.__class__.__name__, error.original), file=sys.stderr)
        elif hasattr(error, 'original'):
            traceback.print_tb(error.original.__traceback__)

    def initialize_cog(self):
        """Saves the original cmd error handler"""
        self.bot.on_command_error_backup = copy_func(self.bot.on_command_error)
        self.bot.on_command_error = self._on_command_error

    def __unload(self):
        """Readds the original error handler"""
        self.bot.on_command_error = self.bot.on_command_error_backup
        del self.bot.on_command_error_backup

def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
