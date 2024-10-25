import time
import settings
from utils import is_command_channel, EMBED_COLOR
from discord import Embed
from discord.ext import commands

class ModuleCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.failed_modules = []

    async def load_modules(self):
        """Carrega todos os módulos da pasta 'cogs' durante a inicialização e registra o tempo de carregamento."""
        print("Loading modules...")
        for cog_file in settings.COGS_DIR.glob("*.py"):
            if cog_file.name != "__init__.py":
                # Verifica se o módulo já está carregado
                module_name = f"cogs.{cog_file.name[:-3]}"
                if module_name not in self.bot.extensions:
                    try:
                        start_time = time.time()
                        await self.bot.load_extension(module_name)
                        end_time = time.time()

                        load_time = (end_time - start_time) * 1000
                        print(f"Loaded module {cog_file.name[:-3]} ... {load_time:.2f} ms")
                    except Exception as e:
                        exc = f"{type(e).__name__}: {e}"
                        print(f"Failed to load cog {cog_file.name[:-3]}\n{exc}")
                        self.failed_modules.append(cog_file.name[:-3])

        print('-' * 72)

    @commands.command(name="listmodules", help="Lista todos os módulos carregados.")
    @is_command_channel()
    async def listmodules(self, ctx):
        """Lista todos os módulos carregados no bot, indicando se algum falhou."""
        # List Loaded Modules
        loaded_modules = [module.replace("cogs.", "") for module in self.bot.extensions.keys() if module.startswith("cogs.")]

        if loaded_modules:
            description = "\n".join(
                f"[{'**FAIL**' if module in self.failed_modules else '**OK**'}] ... {module}"
                for module in loaded_modules
            )
            embed = Embed(
                title=":gear: Módulos carregados",
                description=description,
                color=EMBED_COLOR['nominal'] if not self.failed_modules else EMBED_COLOR['attention']
            )
        else:
            embed = Embed(
                title=":warning: **Nenhum módulo carregado.**",
                color=EMBED_COLOR['attention']
            )

        await ctx.send(embed=embed)

    @commands.command(name="reload", help="Recarrega todos os módulos.")
    @is_command_channel()
    async def reload(self, ctx):
        """Recarrega todos os módulos na pasta 'cogs' e registra o tempo de carregamento."""
        print("\nReloading modules...")

        self.failed_modules = []

        await ctx.send("Recarregando módulos...")
        for cog_file in settings.COGS_DIR.glob("*.py"):
            if cog_file.name != "__init__.py":
                module_name = f"cogs.{cog_file.name[:-3]}"
                try:
                    # Verifica se o módulo já está carregado
                    if module_name in self.bot.extensions:
                        start_time = time.time()  # Inicia a contagem de tempo
                        await self.bot.reload_extension(module_name)
                        end_time = time.time()  # Finaliza a contagem de tempo

                        load_time = (end_time - start_time) * 1000  # Converte para milissegundos
                        print(f"Reloaded module {cog_file.name[:-3]} ... {load_time:.2f} ms")
                    else:
                        print(f"Módulo {cog_file.name[:-3]} não está carregado, ignorando.")
                except Exception as e:
                    exc = f"{type(e).__name__}: {e}"
                    print(f"Falha ao recarregar o módulo {cog_file.name[:-3]}\n{exc}")
                    self.failed_modules.append(cog_file.name[:-3])
                    await ctx.send(f"Falha ao recarregar o módulo {cog_file.name[:-3]}.\n")

        print('-' * 80)

async def setup(bot):
    cog = ModuleCommands(bot)
    await cog.load_modules()  # Carrega os módulos ao inicializar
    await bot.add_cog(cog)
