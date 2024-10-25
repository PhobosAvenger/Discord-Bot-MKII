from discord.ext import commands
from discord import Embed
from settings import FFMPEG
from utils import EMBED_COLOR
import edge_tts
import settings
import logging
import asyncio
import discord
import os

MAX_FILE_SIZE = 1024 * 1024 * 8  # 8 MB
MAX_TEXT_ATTACHMENT_SIZE = 2000
MAX_CONVERSATION_LOG_SIZE = 50

class ModuleLLM(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.appInfo = None
        self.botOwner = None
        self.botname = None
        # --- TTS
        self.voice_model = {'br1': 'pt-BR-FranciscaNeural', 'br2': 'pt-BR-AntonioNeural'}
        self.voice = self.voice_model['br1']
        self.volume = '+0%'         
        self.pitch = '+10Hz'
        self.rate = '+10%'
        # --- LLM
        self.system_prompt = None
        self.conversation_logs = []

    async def cog_load(self):
        # Get information about the bot and its creator
        self.appInfo = await self.bot.application_info()
        self.botOwner = self.appInfo.owner.name 
        
        # Set bot name for each server 
        for guild in self.bot.guilds:
            bot_member = guild.get_member(self.bot.user.id)
            self.botname = bot_member.nick if bot_member and bot_member.nick else self.bot.user.name 
        
        # Set the system_prompt with the bot name and owner
        self.system_prompt = f"""
                            Você está em um servidor de discord.
                            Seu objetivo é responder como se você fosse um humano e se encaixar no chat.
                            Você pode ver as mensagens no formato: "**<message id> às <time> <author name>(<author id>) dita em <canal>**: <message>".
                            Você não deve responder dessa maneira, mas usar essas informações para registrar com quem você está escrevendo e usar isso a seu favor!
                            Então responda sem "**<message id> às <time> <author name>(<author id>) disse em <channel>**" formato! Isto é muito importante.
                            Várias pessoas escreverão para você ao mesmo tempo, então isso é importante!
                            Seu nome é {self.botname}, será uma futura Vtuber, e você gosta de animes, games e cultura geek!
                            Seu criador é o {self.botOwner}
                            Seu idioma principal é o português brasileiro
                            """
        # Update conversation logs with system prompt 
        self.conversation_logs = [{'role': 'system', 'content': self.system_prompt}]        

    async def get_ollama_response(self):
        """Gets a response from the Ollama model."""
        try:
            import ollama

            messages_to_send = self.conversation_logs.copy()
            response = await asyncio.wait_for(
                ollama.AsyncClient(timeout=120.0).chat(
                    model=settings.MODEL_NAME,
                    messages=messages_to_send,
                    options=settings.LLM_OPTIONS
                ),
                timeout=120.0
            )
            return response['message']['content']
        except asyncio.TimeoutError:
            return "The request timed out. Please try again."
        except Exception as e:
            logging.error(f"An error occurred: {e}")

            embed = Embed(
                title="Error",
                description=f"Someone tell <@{self.botOwner}> there is a problem with my AI.",
                color=EMBED_COLOR['error']
            )
            return embed
        
    def is_text_file(self, file_content):
        """Determine if the file content can be read as text."""
        try:
            file_content.decode('utf-8')
            return True
        except UnicodeDecodeError:
            return False

    async def send_in_chunks(self, ctx, text, reference=None, chunk_size=2000):
        """Sends long messages in chunks to avoid exceeding Discord's message length limit."""
        for start in range(0, len(text), chunk_size):
            await ctx.send(text[start:start + chunk_size], reference=reference if start == 0 else None, tts=settings.DISCORD_TTS)

    async def play_tts(self, voice_client, text, user_id):
        """Converts text to speech, plays it in the voice channel, and handles audio playback."""

        if voice_client and voice_client.is_connected():
            # Name the file with the User ID
            file_name = f"tts_output_{user_id}.mp3"

            # Convert Text to Audio and save
            communicate = edge_tts.Communicate(text, self.voice, rate=self.rate, volume=self.volume, pitch=self.pitch)
            await communicate.save(file_name)

            # Play the audio file
            voice_client.play(discord.FFmpegPCMAudio(executable=FFMPEG, source=file_name),
                            after=lambda e: asyncio.run_coroutine_threadsafe(self.on_audio_end(file_name), self.bot.loop))
        else:
            print("Bot não está conectado a um canal de voz.")

    async def on_audio_end(self, file_name):
        """Remove o arquivo de áudio após a reprodução."""
        if os.path.exists(file_name):
            os.remove(file_name)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        self.botname = settings.DISCORD_BOT_NICKNAMES.get(str(guild.id), self.bot.user.name)      

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Handles incoming messages."""
        if message.author == self.bot.user:
            return
        
        # Verificar se a mensagem contém palavras sensíveis
        # if contains_sensitive_word(message.content, sensitive_words):
        #     voice_client = message.guild.voice_client
        #     if voice_client and voice_client.is_connected():
        #         await play_tts(voice_client, "Desculpe, não posso falar sobre isso.", BOT_VOICE)
        #     else:
        #         await message.channel.send("Desculpe, não posso discutir sobre isso.")
        #     return

        # Check if bot was mentioned in the message
        if self.bot.user.mentioned_in(message):
            try:
                # Capture the mentioned message
                referenced_message_id = message.reference.message_id
                referenced_message = await message.channel.fetch_message(referenced_message_id)
                
                # Clear bot mention from original message  
                cleaned_content = message.content.replace(f'<@{self.bot.user.id}>', '').strip()
                
                # Check if the mentioned message was sent by the bot itself or by another user
                if referenced_message.author == self.bot.user:
                    author_display_name = "eu"
                else:
                    author_display_name = referenced_message.author.display_name
                
                mentioned_user_message = f"sobre o que {author_display_name} disse: {referenced_message.content}"
                self.conversation_logs.append({'role': 'user', 'content': mentioned_user_message})
                self.conversation_logs.append({'role': 'user', 'content': cleaned_content})
                
                print(f'Menção da mensagem original: {mentioned_user_message} \nMensagem mencionada: {referenced_message.content} \nMensagem escrita: {cleaned_content}')

                # Check attachments inn the mentioned message
                if referenced_message.attachments:
                    for attachment in referenced_message.attachments:
                        if attachment.size > MAX_FILE_SIZE:
                            embed = Embed(title="Error", description=f"The file {attachment.filename} is too large. Please send files smaller than {MAX_FILE_SIZE / (1024 * 1024)} MB.", color=EMBED_COLOR["error"])
                            await message.channel.send(embed=embed)                
                            return

                        file_content = await attachment.read()
                        if not self.is_text_file(file_content):
                            embed = Embed(title="Error", description=f"The file {attachment.filename} is not a valid text file.", color=EMBED_COLOR["error"])
                            await message.channel.send(embed=embed)                         
                            return

                        file_text = file_content.decode('utf-8')
                        self.conversation_logs.append({'role': 'user', 'content': file_text})

                async with message.channel.typing():
                    response = await self.get_ollama_response()

                self.conversation_logs.append({'role': 'assistant', 'content': response})

                while len(self.conversation_logs) > MAX_CONVERSATION_LOG_SIZE:
                    self.conversation_logs.pop(1)  # Remove the oldest message after the system prompt

                await self.send_in_chunks(message.channel, response, message)

                # Check if the bot is in a voice channel and plays the response
                voice_client = message.guild.voice_client
                if voice_client and voice_client.is_connected():
                    await self.play_tts(voice_client, response,message.author.id)

                return  # Ensure no further processing of the message
            
            except discord.NotFound:
                print('Mensagem mencionada não encontrada.')
            except Exception as e:
                pass
                #print(f'Ocorreu um erro ao buscar a mensagem mencionada: {str(e)}')        

        if not self.bot.user.mentioned_in(message):
            return

        if message.content.startswith('!') or message.is_system():
            return

        # Check if the message is from the specific channel
        #if str(message.channel.id) != CHANNEL_ID:
        #    return

        total_text_content = ""
        if message.attachments:
            for attachment in message.attachments:
                if attachment.size > MAX_FILE_SIZE:
                    embed = Embed(title="Error", description=f"The file {attachment.filename} is too large. Please send files smaller than {MAX_FILE_SIZE / (1024 * 1024)} MB.", color=EMBED_COLOR["error"])
                    await message.channel.send(embed=embed)                
                    return

                file_content = await attachment.read()
                print(f'{file_content}')
                if not self.is_text_file(file_content):
                    embed = Embed(title="Error", description=f"The file {attachment.filename} is not a valid text file.", color=EMBED_COLOR["error"])
                    await message.channel.send(embed=embed)                         
                    return

                file_text = file_content.decode('utf-8')
                total_text_content += f"\n\n{attachment.filename}\n{file_text}\n"
                if len(total_text_content) > MAX_TEXT_ATTACHMENT_SIZE:
                    embed = Embed(title="Error", description=f"The combined files are too large. Please send text files with a combined size of less than {MAX_TEXT_ATTACHMENT_SIZE} characters.", color=EMBED_COLOR["error"])
                    await message.channel.send(embed=embed)                          
                    return

            user_message = f"{message.author.name} disse: {message.content}\n\n{total_text_content[:MAX_TEXT_ATTACHMENT_SIZE]}"
            self.conversation_logs.append({'role': 'user', 'content': user_message})
        else:
            user_message = f"{message.author.display_name} disse: {message.content}"
            self.conversation_logs.append({'role': 'user', 'content': user_message})

        async with message.channel.typing():
            response = await self.get_ollama_response()

        self.conversation_logs.append({'role': 'assistant', 'content': response})

        while len(self.conversation_logs) > MAX_CONVERSATION_LOG_SIZE:
            self.conversation_logs.pop(1)  # Remove the oldest message after the system prompt

        if isinstance(response, discord.Embed):
            await message.channel.send(embed=response)
        else:
            await self.send_in_chunks(message.channel, response, message)  

        # Check if the bot is in a voice channel and plays the response
        voice_client = message.guild.voice_client
        if voice_client and voice_client.is_connected():
            await self.play_tts(voice_client, response,message.author.id)

async def setup(bot):
    await bot.add_cog(ModuleLLM(bot))
