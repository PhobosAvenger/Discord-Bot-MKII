import discord
from discord.ext import commands
from settings import FFMPEG
from utils import is_command_channel
import asyncio
import os
import edge_tts

class TTSmodule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = asyncio.Queue()
        self.is_playing = False
        self.voice_model = {'br1':'pt-BR-FranciscaNeural','br2':'pt-BR-AntonioNeural'}
        self.voice = self.voice_model['br1']
        self.volume  = '+0%'         
        self.pitch   = '+20Hz'
        self.rate    = '+20%'

    @commands.command(name='speak')
    @is_command_channel()
    async def speak(self, ctx, *, text):
        # Add text to Queue
        await self.queue.put((ctx, text))
        
        # If doesn't playing, start play audio
        if not self.is_playing:
            await self.play_next_audio()

    async def play_next_audio(self):
        if self.queue.empty():
            self.is_playing = False
            return

        self.is_playing = True

        # Get the next item from queue (ctx and text)
        ctx, text = await self.queue.get()

        # Check if bot is connected in the voice channel
        voice_client = ctx.guild.voice_client

        if voice_client and voice_client.is_connected():
            # Convert text to audio using edgeTTS and save to temp file
            communicate = edge_tts.Communicate(text, self.voice, rate=self.rate, volume=self.volume , pitch=self.pitch)
            file_name = f"tts_output_{ctx.author.id}.mp3"
            await communicate.save(file_name)

            # Plays the audio file in the voice channel 
            voice_client.play(discord.FFmpegPCMAudio(executable=FFMPEG, source=file_name),
                              after=lambda e: self.bot.loop.create_task(self.on_audio_end(file_name)))
        else:
            await ctx.send('Não estou conectado a um canal de voz.')
            self.is_playing = False  # Set as False if not can reproduce audio

    async def on_audio_end(self, file_name):
        # Delete the audio file after playback ends
        if os.path.exists(file_name):
            os.remove(file_name)
        
        # Wait one second after chek the next playback
        await asyncio.sleep(1)
        
        # Play the next audio from queue
        await self.play_next_audio()

async def setup(bot):
    await bot.add_cog(TTSmodule(bot))
