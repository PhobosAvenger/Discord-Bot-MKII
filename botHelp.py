import discord
import settings
from utils import is_command_channel
from discord.ext import commands
from discord import app_commands

class Help(commands.HelpCommand):
    def __init__(self, **options):
        super().__init__(**options)

    @is_command_channel()
    async def send_bot_help(self, mapping):
        ctx = self.context
        bot = self.context.bot

        embed = discord.Embed(
            title="Hello there!",
            description=f"My name is {settings.DISCORD_BOT_NICKNAMES.get(str(ctx.guild.id))}, and I hope I can be of service to you!\nHere is a list of selected commands I can do!",
            color=discord.Color.blue()
        )
        embed.set_author(name=bot.user.name, icon_url=bot.user.avatar.url if bot.user.avatar else bot.user.default_avatar.url)
        embed.set_thumbnail(url=bot.user.avatar.url if bot.user.avatar else bot.user.default_avatar.url)
        embed.set_footer(text="Made with Python")
        embed.timestamp = discord.utils.utcnow()

        # Filter an add only desired cogs commands
        for cog, commands in mapping.items():

            if cog is None or cog.qualified_name == "ModuleCommands":
                continue

            # Filter usable commands
            filtered_commands = await self.filter_commands(commands, sort=True)
            if filtered_commands:
                name = cog.qualified_name
                value = "\n".join(f"`{ctx.clean_prefix}{c.name}` - {c.short_doc or 'No description'}" for c in filtered_commands)
                embed.add_field(name=f"__**{name}**__", value=value, inline=False)

        # Slash commands and groups
        slash_commands = bot.tree.get_commands()  # Get all slash commands
        categories = [c for c in slash_commands if self.is_command_group(c)]
        misc_commands = [c for c in slash_commands if not self.is_command_group(c)]  # Non-categorized slash commands

        # Add misc slash commands (without groups)
        if misc_commands:
            embed.add_field(
                name="Slash Commands (No Category)",
                value=self.create_field_for_commands(misc_commands),
                inline=False
            )

        # Add categorized slash commands (groups)
        for category in categories:
            embed.add_field(
                name=f"{category.name.capitalize()} • {category.description or 'No description'}",
                value=self.create_field_for_commands(category.options, parent_command=category),
                inline=False
            )

        await ctx.send(embed=embed)

    def is_command_group(self, command: app_commands.AppCommand):
        """Verifica se o comando é um grupo (subcomando ou grupo de subcomandos)"""
        return command.type == discord.AppCommandType.chat_input and any(
            opt.type in [discord.AppCommandOptionType.sub_command, discord.AppCommandOptionType.sub_command_group]
            for opt in command.options
        )

    def create_field_for_commands(self, commands, parent_command=None):
        """Cria uma string para listar comandos dentro de um campo de embed"""
        if parent_command:
            command_descriptions = [f"</{parent_command.name} {c.name}:{parent_command.id}>" for c in commands]
        else:
            command_descriptions = [f"`/{c.name}` - {c.description or 'No description'}" for c in commands]

        return '\n'.join(command_descriptions)

async def setup(bot):
    bot.help_command = Help()
