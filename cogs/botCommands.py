import discord
import settings
import time
import os
from utils import convert_num_to_emoji, emoji_numbers, EMBED_COLOR
from utils import is_command_channel
from discord.ext import commands
from discord import Embed
from datetime import datetime

# bot up-time
start_time = time.time()

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Envia uma mensagem")
    @commands.has_permissions(administrator=True)
    @is_command_channel()
    async def say(self, ctx, *, msg):
        await ctx.send(msg)

    @commands.command(name="setActivity")
    @commands.has_permissions(administrator=True)  # Admin only
    @is_command_channel()
    async def setActivity(self, ctx, activity_type: str, *, activity_name: str):
        """
        Altera a atividade do bot. Tipos de atividade permitidos: playing, watching, listening, competing.
        Exemplo de uso: !setActivity playing Jogando Minecraft
        """
        activity_type = activity_type.lower()

        if activity_type == "playing":
            activity = discord.Game(name=activity_name)
        elif activity_type == "watching":
            activity = discord.Activity(type=discord.ActivityType.watching, name=activity_name)
        elif activity_type == "listening":
            activity = discord.Activity(type=discord.ActivityType.listening, name=activity_name)
        elif activity_type == "competing":
            activity = discord.Activity(type=discord.ActivityType.competing, name=activity_name)
        elif activity_type == "custom":
            activity = discord.CustomActivity(name=activity_name)
        else:
            await ctx.send("Tipo de atividade inválido. Use: `playing`, `watching`, `listening`, ou `competing`.")
            return

        # Set the bot activity
        await self.bot.change_presence(activity=activity)
        await ctx.send(f"Atividade do bot alterada para **{activity_type}** `{activity_name}`.")

class BotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file_path = os.path.abspath("nicknames.json")
        self.nicknames = settings.DISCORD_BOT_NICKNAMES
    
    @commands.command(name='join', help='Entra no mesmo canal de voz onde você está')
    @is_command_channel()
    async def join(self, ctx): 
        if ctx.author.voice:  # Check if author is in voice channel
            channel = ctx.author.voice.channel  # Get the author voice channel
            
            voice_client = ctx.guild.voice_client  # Get the server VoiceClient 
            
            if voice_client:
                await voice_client.move_to(channel)
            else:
                voice_client = await channel.connect()
            
            print(f' -- Connected on the voicechannel [{channel}]')
        else:
            await ctx.send('Você precisa estar em um canal de voz para usar este comando.')

    @commands.command(name='leave', help='Desconecta o bot de qualquer canal de voz')
    @is_command_channel()
    async def leave(self, ctx):
        voice_client = ctx.guild.voice_client
        
        if voice_client and voice_client.is_connected():
            await voice_client.disconnect()
        else:
            await ctx.send('Não estou conectado a um canal de voz.')

    @commands.command(name="setnick", help="Define o apelido do bot no servidor.")
    @commands.has_permissions(manage_nicknames=True)
    @is_command_channel()
    async def setnick(self, ctx, *, new_nickname: str):
        """Define o apelido do bot e armazena no arquivo JSON."""
        try:
            await ctx.guild.me.edit(nick=new_nickname)

            self.nicknames[str(ctx.guild.id)] = new_nickname
            settings.save_nicknames(self.nicknames)

            print(f"Nickname changed to '{new_nickname}' from server [{ctx.guild.name}]")
            await ctx.send(f"Apelido alterado para: `{new_nickname}` e salvo.")
        except discord.Forbidden:
            await ctx.send("Não tenho permissão para alterar o apelido.")
        except Exception as e:
            await ctx.send(f"Ocorreu um erro: {e}")

    @commands.command(name="resetnick", help="Reseta o apelido do bot no servidor.")
    @commands.has_permissions(manage_nicknames=True)
    @is_command_channel()
    async def resetnick(self, ctx):
        """Reseta o apelido do bot para o nome padrão."""
        try:
            await ctx.guild.me.edit(nick=ctx.bot.user.name)

            self.nicknames[str(ctx.guild.id)] = ctx.bot.user.name
            settings.save_nicknames(self.nicknames)

            print(f"Nickname set to default from server [{ctx.guild.name}]")
            await ctx.send("Apelido resetado para o nome padrão.")
        except discord.Forbidden:
            await ctx.send("Não tenho permissão para alterar o apelido.")
        except Exception as e:
            await ctx.send(f"Ocorreu um erro: {e}")

class BasicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emojis = emoji_numbers

    @commands.command(help="Diz olá ao usuário.")
    @is_command_channel()
    async def hello(self, ctx):
        await ctx.send(f"Olá, {ctx.author.mention}!")

    @commands.command(help="Mostra informações do servidor.")
    @is_command_channel()
    async def info(self, ctx):
        guild = ctx.guild
        count = convert_num_to_emoji(guild.member_count)
        
        embed = Embed(
            title = f":globe_with_meridians:  Servidor **{guild.name}**",
            description=f'Membros {count}',
            color=EMBED_COLOR['help']
        )
        await ctx.send(embed=embed)

    @commands.command(name='about', help='Mostra informações sobre o bot.')
    @is_command_channel()
    async def about(self, ctx):
        """Mostra informações sobre o bot."""
        current_time = time.time()
        uptime_seconds = int(current_time - start_time)
        uptime_str = time.strftime("%H:%M:%S", time.gmtime(uptime_seconds))

        # Obtain bot owner information
        creator = await ctx.bot.application_info()
        owner = creator.owner

        creator_name = owner.display_name
        creator_photo_url = owner.avatar.url if owner.avatar else owner.default_avatar.url
        bot_model = 'Modelo do Bot'
        uptime = uptime_str

        # Embed
        embed = discord.Embed(title="Sobre o Bot", color=EMBED_COLOR['about'])
        embed.set_thumbnail(url=creator_photo_url)
        embed.add_field(name="Criador", value=creator_name, inline=False)
        embed.add_field(name="Modelo", value=bot_model, inline=False)
        embed.add_field(name="Tempo de Uso", value=uptime, inline=True)

        await ctx.send(embed=embed)

class ServerInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Mostra diversas informações sobre o servidor.")
    @is_command_channel()
    async def serverinfo(self, ctx):
        guild = ctx.guild
        owner = await self.bot.fetch_user(guild.owner_id)

        # Server creation date
        created_at = guild.created_at.strftime("%d/%m/%Y, %H:%M:%S")

        # Membr count
        member_count = convert_num_to_emoji(guild.member_count)

        # Channel count
        #text_channels = len(guild.text_channels)
        #voice_channels = len(guild.voice_channels)

        # Creating embed
        embed = Embed(
            title = f":globe_with_meridians: Servidor **{guild.name}**",
            color=EMBED_COLOR['help'],
            timestamp=datetime.utcnow() 
        )

        # Owner Mention
        owner_mention = f"<@{owner.id}>"

        # Add fields with info
        embed.add_field(name="👑 Dono", value=owner_mention, inline=True)
        embed.add_field(name="👥 Membros ", value=f"{member_count}", inline=True)
        embed.add_field(name="📅 Criado em", value=f"{created_at}", inline=False)

        # displaying server icon as thumbnail
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)

        # Footer opitional (Display who called the command)
        embed.set_footer(text=f"Comando requisitado por {ctx.author.name}", icon_url=ctx.author.avatar.url)

         # Send the embed
        await ctx.send(embed=embed) 

async def setup(bot):
    await bot.add_cog(AdminCommands(bot))
    await bot.add_cog(BotCommands(bot))
    await bot.add_cog(BasicCommands(bot))
    await bot.add_cog(ServerInfo(bot))
