import settings
import discord
from discord import Embed
from utils import EMBED_COLOR

logger = settings.logging.getLogger("bot")

class StartupBot:
    def __init__(self, guild_name, embed_color):
        self.guild_name = guild_name
        self.embedColor = embed_color

    def create_embed(self):
        embed = Embed(
            title=":white_check_mark: Bot On-line",
            description=f'Olá, **{self.guild_name}**! Estou online e pronto para ajudar!',
            color=self.embedColor
        )
        return embed

async def startupMessage(bot):
    
    # Define a presença do bot
    activity = discord.Game(name=settings.DISCORD_BOT_MESSAGE)
    await bot.change_presence(status=discord.Status.online, activity=activity)

    # Loads individual nickname file for each server
    settings.load_nicknames(bot)

    # Send startup message to each guild
    for guild in bot.guilds:
        try:
            # Try searching for a textchannel by name allowed in the guild
            channel = next(
                (c for c in guild.text_channels if c.name in settings.ALLOWED_COMMAND_CHANNELS and c.permissions_for(guild.me).send_messages),
                None
            )

            # if not found allowed channel,try to use the first allowed channel
            if not channel:
                channel = next((c for c in guild.text_channels if c.permissions_for(guild.me).send_messages), None)

            if channel:
                startup_message = StartupBot(guild.name, EMBED_COLOR['welcome'])
                embed = startup_message.create_embed()
                await channel.send(embed=embed)

                # Check if Guild ID is in nicknames dict
                new_nick = settings.DISCORD_BOT_NICKNAMES.get(str(guild.id))
                if new_nick:
                    await guild.me.edit(nick=new_nick)
                    #print(f"Nickname do bot atualizado para: [{new_nick}] na guild [{guild.name}]")
                else:
                    print(f"Guild {guild.id} não encontrada no arquivo de nicknames.")
            else:
                print(f"Não foi possível encontrar um canal para enviar a mensagem de startup na guild {guild.name}.")
        except Exception as e:
            print(f"Erro ao enviar mensagem para a guild {guild.name}: {e}")

