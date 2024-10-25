import os
import settings
import discord
from discord.ext import commands
from startupBot import startupMessage
from botHelp import Help

logger = settings.logging.getLogger("bot")

def run():
    os.system('cls')

    Intents = discord.Intents.default()
    Intents.message_content = True

    bot = commands.Bot(command_prefix="!",help_command=Help(), intents=Intents)

    @bot.event 
    async def on_ready():
        await bot.load_extension("moduleLoader")
        await startupMessage(bot)
        
        logger.info(f"User: {bot.user.name} (ID: {bot.user.id})")                                 
                 
    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Handled error globally")
        elif isinstance(error, commands.CheckFailure):
            allowed_channels = ', '.join(f"#{channel}" for channel in settings.ALLOWED_COMMAND_CHANNELS)
            await ctx.send(f"Este comando só pode ser usado nos canais: {allowed_channels}.")
        else:
            pass
                         
    bot.run(settings.DISCORD_TOKEN, root_logger=True)

if __name__ == "__main__":
    run()
