import discord
from discord.ext import commands
from utils import is_command_channel
import aiohttp

class GenshinAPI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='genshin')
    @is_command_channel()
    async def genshin(self, ctx, userID: str):
        """Comando para buscar informações do perfil Genshin de um usuário com base no ID."""
        # URL from API with userID
        url = f"https://akasha.cv/api/user/{userID}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                # Check if response has been sucessfull (status 200)
                if response.status == 200:
                    data = await response.json()

                    # Check if data is invalid
                    account = data.get('data', {}).get('account', {})
                    if not account or (account.get('profilePictureLink') is None and account.get('nameCardLink') is None):
                        await ctx.send(f"ID de usuário `{userID}` não encontrado ou inválido.")
                        return

                    player_info = account.get("playerInfo", {})
                    
                    # Extracting main data from JSON
                    nickname = player_info.get("nickname", "Desconhecido")
                    level = int(player_info.get("level", 0))
                    world_level = int(player_info.get("worldLevel", 0))
                    signature = player_info.get("signature", "Sem assinatura")
                    achievements = int(player_info.get("finishAchievementNum", 0))
                    tower_floor = int(player_info.get("towerFloorIndex", 0))
                    tower_level = int(player_info.get("towerLevelIndex", 0))

                    # Get image links
                    profile_picture = account.get("profilePictureLink", "")
                    namecard_link = account.get("nameCardLink", "")

                    # Create embed based with json data
                    embed = discord.Embed(
                        title=f"Perfil de {nickname}",
                        description=f"Nível: {level}\nMundo: {world_level}\nAssinatura: {signature}",
                        color=discord.Color.blue()
                    )

                    # Add achievements and Abyss floor level information
                    embed.add_field(name="Realizações Completas", value=str(achievements), inline=True)
                    embed.add_field(name="Andares da Torre", value=f"Andar {tower_floor}, Nível {tower_level}", inline=True)

                    # Add images (Profile picture and namecard)
                    if profile_picture:
                        embed.set_thumbnail(url=profile_picture)
                    if namecard_link:
                        embed.set_image(url=namecard_link)

                    # Defines the embed author (Display who called the command)
                    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)

                    # Send the embed
                    await ctx.send(embed=embed)
                else:
                    # Custom error message with status response 
                    await ctx.send(f"Erro ao consultar o usuário com ID `{userID}`. Verifique se o ID está correto. Status do erro: {response.status}.")


async def setup(bot):
    await bot.add_cog(GenshinAPI(bot))
