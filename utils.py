import settings
import discord
from discord.ext import commands

EMBED_COLOR = {
    "nominal": discord.Color.green(), 
    "error": discord.Color.red(), 
    "attention": discord.Color.orange(),
    "welcome": discord.Color.blue(), 
    "help": discord.Color.magenta(),
    "about": discord.Color.purple()
}

emoji_numbers = {
    '0': '0️⃣',
    '1': '1️⃣',
    '2': '2️⃣',
    '3': '3️⃣',
    '4': '4️⃣',
    '5': '5️⃣',
    '6': '6️⃣',
    '7': '7️⃣',
    '8': '8️⃣',
    '9': '9️⃣'
}

def convert_num_to_emoji(number):
    """Converte o número em formato de string para emojis."""
    return ''.join(emoji_numbers[digit] for digit in str(number))

def is_command_channel():
    async def predicate(ctx):
        return ctx.channel.name in settings.ALLOWED_COMMAND_CHANNELS
    return commands.check(predicate)