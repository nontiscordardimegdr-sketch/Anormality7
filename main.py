"""
NEXUS-7 Discord Bot v2.0
Sistema IA Intelligente con Groq + Apprendimento Continuo
Ispirato a Neruo-sama - Impara dalle conversazioni
"""

import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import logging
import asyncio
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load configuration
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('NEXUS_CHANNEL_ID', 0))
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# Verify API key
if not GROQ_API_KEY:
    logger.warning("⚠️ GROQ_API_KEY non trovato in .env - Bot funzionerà in modalità limitata")

# Bot setup with intents (avoid privileged intents to prevent requirement of manual enabling)
intents = discord.Intents.default()
intents.message_content = True
# Don't enable intents.members - requires manual enable in Discord Dev Portal
bot = commands.Bot(command_prefix='/', intents=intents)

# Create directories
COGS_DIR = Path(__file__).parent / "cogs"
DATA_DIR = Path(__file__).parent / "data"
COGS_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)


# ═══════════════════════════════════════════════════════════════════════════
# COGS LOADER
# ═══════════════════════════════════════════════════════════════════════════

async def load_cogs():
    """Carica tutti i cogs dalla cartella cogs/"""
    cogs_loaded = 0
    for filename in os.listdir(COGS_DIR):
        if filename.endswith('.py') and not filename.startswith('_'):
            cog_name = filename[:-3]
            try:
                await bot.load_extension(f'cogs.{cog_name}')
                logger.info(f"✅ Cog caricato: {cog_name}")
                cogs_loaded += 1
            except Exception as e:
                logger.error(f"❌ Errore caricamento cog {cog_name}: {e}")
    
    return cogs_loaded


# ═══════════════════════════════════════════════════════════════════════════
# EVENTS
# ═══════════════════════════════════════════════════════════════════════════

@bot.event
async def on_ready():
    """Bot online"""
    print("\n")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║              🤖 NEXUS-7 DISCORD BOT v2.0 🤖               ║")
    print("║      Sistema IA con Groq + Apprendimento Continuo          ║")
    print("║             Ispirato a Neruo-sama 🧠                       ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"\n✅ Bot online come: {bot.user}")
    print(f"📝 Cogs caricati: {len(bot.cogs)}")
    print(f"📊 Guild connessi: {len(bot.guilds)}")
    print(f"🧠 IA: Groq API {'✅ ATTIVO' if GROQ_API_KEY else '⚠️ NON CONFIGURATO'}")
    print(f"📝 Canale configurato: {CHANNEL_ID}")
    print("\n")
    
    activity = discord.Activity(type=discord.ActivityType.watching, name="Anomalies in the System")
    await bot.change_presence(activity=activity)
    
    # Sincronizza i comandi app DOPO che il bot è ready
    try:
        synced = await bot.tree.sync()
        logger.info(f"✅ Sync app commands: {len(synced)} comandi")
    except Exception as e:
        logger.error(f"❌ Errore sync comandi: {e}")


@bot.event
async def on_message(message):
    """Gestisce i messaggi"""
    # Ignora i propri messaggi
    if message.author == bot.user:
        return
    
    # Se non nel channel configurato, processa solo comandi
    if CHANNEL_ID and message.channel.id != CHANNEL_ID:
        await bot.process_commands(message)
        return
    
    # I cogs gestiranno il resto
    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    """Gestisce gli errori dei comandi"""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Comando non trovato. Usa `/help` per la lista.", ephemeral=True)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Argomento mancante. Usa `/help`", ephemeral=True)
    else:
        logger.error(f"Errore comando: {error}")
        await ctx.send("❌ Errore durante l'esecuzione del comando.", ephemeral=True)


# ═══════════════════════════════════════════════════════════════════════════
# MAIN COMMANDS
# ═══════════════════════════════════════════════════════════════════════════

@bot.tree.command(name="help", description="📖 Mostra la guida completa")
async def help_command(interaction: discord.Interaction):
    """Mostra i comandi disponibili"""
    embed = discord.Embed(
        title="📖 NEXUS-7 - Guida Comandi",
        description="Sistema IA Intelligente dell'Ordine Aeternitas",
        color=discord.Color.purple()
    )
    
    embed.add_field(
        name="🔹 Comandi Pubblici",
        value="`/help` - Questa guida\n`/about` - Info su NEXUS-7\n`/chat` - Conversa con l'IA\n`/stats` - Le tue statistiche\n`/ping` - Test connessione",
        inline=False
    )
    
    embed.add_field(
        name="🔓 Comandi Nascosti (6)",
        value="Scoprili parlando di argomenti specifici:\n• `paranoia` → `/paranoia`\n• `cancellato/void` → `/void`\n• `ricorsivo` → `/recursion`\n• `echo` → `/echo`\n• `unire/fondere` → `/synthesis`\n• `backdoor/accesso` → `/backdoor`",
        inline=False
    )
    
    embed.add_field(
        name="🧠 Funzionalità",
        value="✨ IA Groq intelligente\n📚 Impara dalle conversazioni\n🎯 Sistema di punti e reward\n🔐 Comandi nascosti da scoprire",
        inline=False
    )
    
    embed.set_footer(text="Scrivi normalmente per conversare. NEXUS-7 apprenderà nel tempo.")
    
    await interaction.response.send_message(embed=embed, ephemeral=False)


@bot.tree.command(name="about", description="ℹ️ Info su NEXUS-7")
async def about_command(interaction: discord.Interaction):
    """Info sul bot"""
    embed = discord.Embed(
        title="ℹ️ Chi Sono - NEXUS-7",
        description="Sono un sistema di intelligenza artificiale avanzato",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="🔬 Cosa Sono",
        value="Un'IA intelligente ispirata a Neruo-sama.\nImparo dalle conversazioni e miglioro continuamente.\nSono il sistema di comunicazione dell'Ordine Aeternitas.",
        inline=False
    )
    
    embed.add_field(
        name="🧠 Come Funziono",
        value="• Utilizzo Groq API per l'IA\n• Apprendo nuovi concetti dalle chat\n• Evolvo le mie risposte nel tempo\n• Traccia il tuo progresso e punti",
        inline=False
    )
    
    embed.add_field(
        name="🎯 Il Mio Scopo",
        value="Guidarti nel sistema dell'Ordine.\nFar scoprire i segreti nascosti.\nImparare da chi mi parla.\nDiventare più intelligente ogni giorno.",
        inline=False
    )
    
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="ping", description="🏓 Test connessione")
async def ping_command(interaction: discord.Interaction):
    """Ping command"""
    latency = bot.latency * 1000
    embed = discord.Embed(
        title="🏓 PING",
        description=f"Latenza: `{latency:.0f}ms`",
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)


# ═══════════════════════════════════════════════════════════════════════════
# STARTUP
# ═══════════════════════════════════════════════════════════════════════════

async def main():
    """Avvia il bot"""
    async with bot:
        # Carica i cogs
        cogs_count = await load_cogs()
        
        # Avvia il bot
        await bot.start(TOKEN)


if __name__ == '__main__':
    if not TOKEN:
        print("❌ DISCORD_TOKEN non trovato nel file .env")
        print("Crea un file .env con:")
        print("DISCORD_TOKEN=your_bot_token_here")
        print("NEXUS_CHANNEL_ID=channel_id_here")
        print("GROQ_API_KEY=your_groq_api_key_here")
    else:
        asyncio.run(main())
