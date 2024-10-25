import pathlib
import logging
from logging.config import dictConfig
from dotenv import load_dotenv
import discord
import json
import os

load_dotenv()

def load_nicknames(bot):
    global DISCORD_BOT_NICKNAMES

    nickname_file = "./nicknames.json"
    
    # Check if file exists 
    if not os.path.exists(nickname_file):
        default_data = {}
        for guild in bot.guilds:
            default_data[str(guild.id)] = bot.user.name
        
        # Writes the default dict in JSON file 
        with open(nickname_file, "w", encoding="utf-8") as file:
            json.dump(default_data, file, ensure_ascii=False, indent=4)
        print(f"Arquivo não encontrado. Criado novo arquivo: {nickname_file} com dados padrão.")

        # Update the globalvar with default data
        DISCORD_BOT_NICKNAMES = default_data
        return default_data

    # If file exists, try to load content
    try:
        with open(nickname_file, "r", encoding="utf-8") as file:
            data = json.load(file)        

        # Update the variable with loaded data
        DISCORD_BOT_NICKNAMES = data
        return data
    except json.JSONDecodeError:
        print(f"Erro ao decodificar o arquivo JSON: {nickname_file}")
        return {}
    
def save_nicknames(nicknames):
    nickname_file = "./nicknames.json"
    with open(nickname_file, 'w') as f:
        json.dump(nicknames, f, indent=4)

def dotenv_check():
    env_file = ".env"
    
    # Check if the .env file exists
    if not os.path.exists(env_file):
        print(f"{env_file} not found. Creating a new .env file...")
        
        # Default content for .env
        default_content = """# Default .env file
TOKEN_API="YOUR_BOT_TOKEN_HERE"
"""
        # Create the .env file with default content
        with open(env_file, "w") as file:
            file.write(default_content)
        
        print(f"{env_file} created successfully.")
    else:
        pass

def log_file_check():
    # Set path to file
    folder_path = "logs"
    file_path = os.path.join(folder_path, "info.log")
    
    # Check if folder exists
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # check if file exist
    if not os.path.exists(file_path):
        open(file_path, 'w').close()    

# Check if logs folder exists
log_file_check()
# check if .env file exist
dotenv_check()
    
# ------------------------------------------ #

BASE_DIR = pathlib.Path(__file__).parent
CMDS_DIR = BASE_DIR / "cmds"
COGS_DIR = BASE_DIR / "cogs"

FFMPEG = 'ffmpeg'

# ------------------------------------------ #

DISCORD_BOT_NICKNAMES    = {}
DISCORD_BOT_MESSAGE      = ""
DISCORD_TOKEN            = os.getenv("TOKEN_API")
DISCORD_TTS              = False
ALLOWED_COMMAND_CHANNELS = ["bot-cmd", "bot-commands"]

# ------------------------------------------ #

MODEL_NAME = 'llama3.2'
LLM_OPTIONS = {
    'temperature': 1,
     'max_length': 50,
        'num_gpu': 1,
       'main_gpu': 0,
    }

# ------------------------------------------ #

LOGGING_CONFIG = {
    "version": 1,
    "disabled_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)-10s - %(asctime)s - %(module)-15s : %(message)s"
        },
        "standard": {"format": "%(levelname)-10s - %(name)-15s : %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "console2": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "logs/info.log",
            "mode": "w",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "bot": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "discord": {
            "handlers": ["console2", "file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

dictConfig(LOGGING_CONFIG)