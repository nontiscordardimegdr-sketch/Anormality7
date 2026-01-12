"""
Discord Bot Configuration
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Discord Bot Token
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Channel ID where the bot will respond (specific channel for NEXUS-7)
NEXUS_CHANNEL_ID = int(os.getenv('NEXUS_CHANNEL_ID', 0))

# Server/Guild ID (optional, for testing)
GUILD_ID = int(os.getenv('GUILD_ID', 0))

# Bot configuration
BOT_PREFIX = '/'
BOT_NAME = 'NEXUS-7'
BOT_DESCRIPTION = 'Sistema IA dell\'Ordine Aeternitas'

# Feature toggles
ENABLE_PARANOIA = True
ENABLE_EASTER_EGGS = True
ENABLE_HIDDEN_COMMANDS = True
ENABLE_GLITCH_EFFECTS = True

# API settings (if using external API)
GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')

# Database/Storage (using JSON files for simplicity)
DATA_DIR = 'discord_bot/data'
