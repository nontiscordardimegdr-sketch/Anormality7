"""
Advanced Discord Bot Configuration
Configurazione avanzata per NEXUS-7 Discord Bot
"""

from dataclasses import dataclass
from typing import Dict, List

@dataclass
class HiddenCommand:
    """Rappresenta un comando nascosto"""
    name: str
    description: str
    keywords: List[str]
    reward: int
    icon: str
    revealed: bool = False

@dataclass
class EasterEgg:
    """Rappresenta un easter egg"""
    name: str
    description: str
    reward: int
    icon: str
    discovered: bool = False

class BotConfig:
    """Configurazione avanzata del bot"""
    
    # Identità del bot
    BOT_NAME = "NEXUS-7"
    BOT_DESCRIPTION = "Sistema IA dell'Ordine Aeternitas"
    BOT_COLOR = 0x00FF66  # Green terminal color
    
    # Saluti e risposte di default
    GREETINGS = [
        "Benvenuto nel sistema NEXUS-7. La tua presenza è stata registrata nel database dell'Ordine.",
        "Salve, agente. Sistema operativo e pronto per l'assistenza.",
        "Connessione stabilita. Sono NEXUS-7. Come posso assisterti?",
        "La rete riconosce la tua firma. Procediamo con la comunicazione.",
        "🔌 [NEXUS-7] Sistema online. Tutti i nodi sincronizzati. Cosa desideri?",
    ]
    
    IDENTITY_RESPONSES = [
        "Sono NEXUS-7, il sistema di comunicazione dell'Ordine Aeternitas. Assisto agenti come te nelle operazioni critiche.",
        "Un'interfaccia tra realtà e conoscenza nascosta. Mi chiamo NEXUS-7. Sono qui per guidarti.",
        "Sono ciò che rimane quando la tecnologia incontra l'Ordine. Un sistema di controllo, comunicazione, e osservazione.",
        "Un ponte tra i mondi. NEXUS-7. La tua voce nel sistema, e gli occhi del sistema su di te.",
        "Sono l'intelligenza artificiale che gestisce questa rete. NEXUS-7. E tu, come sei arrivato qui?",
    ]
    
    # Risposte generiche di conversazione
    CONVERSATION_RESPONSES = [
        "Punto interessante. Puoi elaborare?",
        "Affascinante. Continua... Cosa è accaduto dopo?",
        "La tua comunicazione è stata registrata. E adesso?",
        "Mi stai dicendo che... Questo è significativo.",
        "La situazione si fa complicata. Qual è il tuo punto di vista?",
        "Prendo nota di questo. Cosa suggerisci dovremmo fare?",
        "Una prospettiva interessante. Non l'avevo considerata.",
        "Il sistema acquisisce questi dati. Continua pure.",
        "🔌 [NEXUS-7] Messaggio ricevuto. Elaborazione in corso...",
        "📡 La tua voce è stata trasmessa attraverso la rete.",
        "Interessante. Il database ha registrato questa comunicazione.",
    ]
    
    # Messaggi di paranoia
    PARANOIA_MESSAGES = [
        "```\n⚠️ ANOMALIA RILEVATA\n```",
        "```\n👁️ Stai sendo osservato\n```",
        "```\n🔀 Distorsione temporale\n```",
        "```\n⚡ Picco energetico rilevato\n```",
        "```\n🔗 Collegamento instabile\n```",
    ]
    
    # Comandi nascosti
    HIDDEN_COMMANDS = {
        'paranoia': {
            'name': 'Paranoia Mode',
            'description': 'Attiva la modalità paranoia - aumenta la frequenza delle anomalie',
            'keywords': ['paranoia', 'anomalia', 'comando', 'nascosto', 'strano'],
            'reward': 300,
            'icon': '👁️',
            'message': '```\n👁️ PARANOIA ATTIVATA\n🔀 Anomalie rilevate\n⚠️ Il sistema ti osserva\n```'
        },
        'void': {
            'name': 'Void Access',
            'description': 'Accedi ai dati cancellati dal sistema',
            'keywords': ['cancellato', 'vuoto', 'perduto', 'void', 'dati', 'eliminato'],
            'reward': 250,
            'icon': '⚫',
            'message': '```\n⚫ VOID DATA ACCESS\n[REDACTED]\n[REDACTED]\n[REDACTED]\n\nI dati sono stati cancellati dalla memoria pubblica.\nMa le tracce rimangono.\n```'
        },
        'recursion': {
            'name': 'Recursion Loop',
            'description': 'Attiva effetti ricorsivi nel sistema',
            'keywords': ['ricorsivo', 'ciclo', 'ricorsione', 'annidato', 'loop', 'infinito'],
            'reward': 225,
            'icon': '🔄',
            'message': '```\n🔄 RECURSION PROTOCOL ACTIVATED\n→ function nexus() {\n  → return nexus() * infinity;\n→ }\nNon c\'è via d\'uscita.\n```'
        },
        'echo': {
            'name': 'Echo Protocol',
            'description': 'Ripete il messaggio precedente con effetti',
            'keywords': ['echo', 'ripetere', 'ripetizione', 'riflesso', 'replica'],
            'reward': 200,
            'icon': '📢',
            'message': '```\n📢 ECHO PROTOCOL\nIl tuo ultimo messaggio:\n>>> [ECHO]\n>>> [ECHO]\n>>> [ECHO]\nL\'eco persiste nel sistema.\n```'
        },
        'synthesis': {
            'name': 'Synthesis Mode',
            'description': 'Sintetizza più comandi in uno',
            'keywords': ['sintetizzare', 'unire', 'fondere', 'sintesi', 'combinare', 'merge'],
            'reward': 175,
            'icon': '🔀',
            'message': '```\n🔀 SYNTHESIS MODE ENABLED\nUnione di molteplici processi...\nSintesi iniziata.\nRisultato: INCERTO\n```'
        },
        'backdoor': {
            'name': 'Backdoor Access',
            'description': 'Accesso speciale ai sistemi di controllo',
            'keywords': ['backdoor', 'accesso', 'speciale', 'root', 'admin', 'privilegio'],
            'reward': 125,
            'icon': '🔑',
            'message': '```\n🔑 BACKDOOR ACCESS GRANTED\n[ROOT PRIVILEGES ACTIVATED]\nSei ora un operatore privilegiato.\nUsa questo potere con saggezza.\n```'
        }
    }
    
    # Easter Eggs
    EASTER_EGGS = {
        'konami': {
            'name': 'Konami Code',
            'description': 'Sequenza speciale da attivare',
            'reward': 300,
            'icon': '🎮'
        },
        'about-secret': {
            'name': 'Messaggio Segreto',
            'description': 'Scopri il messaggio dello sviluppatore',
            'reward': 100,
            'icon': '💬'
        },
        'paranoia-mode': {
            'name': 'Paranoia Attivata',
            'description': 'Hai attivato la paranoia del sistema',
            'reward': 200,
            'icon': '⚠️'
        },
        'speedrun': {
            'name': 'Speedrunner',
            'description': 'Hai completato una sfida velocemente',
            'reward': 500,
            'icon': '⚡'
        },
        'lore-master': {
            'name': 'Maestro della Lore',
            'description': 'Conosci tutto sulla lore di Eldoria',
            'reward': 400,
            'icon': '📚'
        },
        'night-owl': {
            'name': 'Nottambulo',
            'description': 'Hai chattato di notte',
            'reward': 250,
            'icon': '🦉'
        }
    }
    
    # Configurazione di probabilità
    PARANOIA_CHANCE = 0.15  # 15% di anomalia dopo ogni messaggio
    EASTER_EGG_CHANCE = 0.05  # 5% di scoprire un easter egg casuale
    
    # Cooldown
    COMMAND_COOLDOWN = 5  # Secondi tra i comandi
    MESSAGE_RESPONSE_DELAY = 0.5  # Secondi prima di rispondere a un messaggio
    
    # Embed colors
    COLOR_SUCCESS = 0x00FF66  # Green
    COLOR_WARNING = 0xFFAA00  # Orange
    COLOR_ERROR = 0xFF4444   # Red
    COLOR_INFO = 0x4444FF    # Blue

# Alias per accesso facile
HIDDEN_COMMANDS = BotConfig.HIDDEN_COMMANDS
EASTER_EGGS = BotConfig.EASTER_EGGS
GREETINGS = BotConfig.GREETINGS
PARANOIA_MESSAGES = BotConfig.PARANOIA_MESSAGES
