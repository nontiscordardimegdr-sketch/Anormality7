"""
Learning System Cog
Sistema di apprendimento continuo - Come Neruo-sama
Il bot impara dai dati e dalle conversazioni nel tempo
"""

import discord
from discord.ext import commands, tasks
import json
from pathlib import Path
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
DATA_DIR = Path(__file__).parent.parent / "data"


class LearningSystem(commands.Cog):
    """Cog per il sistema di apprendimento continuo"""
    
    def __init__(self, bot):
        self.bot = bot
        self.learning_file = DATA_DIR / "learned_data.json"
        self.stats_file = DATA_DIR / "learning_stats.json"
        self.learned_data = self._load_learned_data()
        self.learning_stats = self._load_stats()
        
        # Avvia il task di salvataggio periodico
        self.save_learning_data.start()
    
    def _load_learned_data(self):
        """Carica i dati imparati"""
        if self.learning_file.exists():
            try:
                with open(self.learning_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Assicurati che tutte le chiavi siano presenti
                    if "concepts" not in data:
                        data["concepts"] = {}
                    if "user_personalities" not in data:
                        data["user_personalities"] = {}
                    if "evolution_timeline" not in data:
                        data["evolution_timeline"] = []
                    if "common_topics" not in data:
                        data["common_topics"] = {}
                    return data
            except:
                pass
        
        return {
            "concepts": {},
            "user_personalities": {},
            "common_topics": {},
            "evolution_timeline": [],
            "last_updated": datetime.now().isoformat()
        }
    
    def _load_stats(self):
        """Carica le statistiche di apprendimento"""
        if self.stats_file.exists():
            try:
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "total_conversations": 0,
            "unique_users": set(),
            "concepts_learned": 0,
            "evolution_level": 1,
            "learning_rate": 0.5
        }
    
    def _save_learning_data(self):
        """Salva i dati imparati"""
        self.learned_data['last_updated'] = datetime.now().isoformat()
        with open(self.learning_file, 'w', encoding='utf-8') as f:
            json.dump(self.learned_data, f, ensure_ascii=False, indent=2)
    
    def _save_stats(self):
        """Salva le statistiche"""
        # Converti il set a lista per il JSON
        stats_to_save = self.learning_stats.copy()
        stats_to_save['unique_users'] = list(stats_to_save.get('unique_users', []))
        with open(self.stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats_to_save, f, ensure_ascii=False, indent=2)
    
    def _extract_concepts(self, text: str):
        """Estrae concetti dal testo"""
        words = text.lower().split()
        concepts = {}
        
        for word in words:
            # Filtra parole significative
            if len(word) > 3 and not word.startswith('/'):
                if word not in self.learned_data["concepts"]:
                    self.learned_data["concepts"][word] = {
                        "count": 0,
                        "first_seen": datetime.now().isoformat(),
                        "importance": 0.5
                    }
                
                self.learned_data["concepts"][word]["count"] += 1
                # Aumenta l'importanza nel tempo (con check di sicurezza)
                if "importance" not in self.learned_data["concepts"][word]:
                    self.learned_data["concepts"][word]["importance"] = 0.5
                self.learned_data["concepts"][word]["importance"] += 0.01
                concepts[word] = self.learned_data["concepts"][word]["count"]
        
        return concepts
    
    def _analyze_user_pattern(self, user_id: int, message: str):
        """Analizza i pattern dell'utente"""
        user_id_str = str(user_id)
        
        if user_id_str not in self.learned_data["user_personalities"]:
            self.learned_data["user_personalities"][user_id_str] = {
                "message_count": 0,
                "avg_length": 0,
                "favorite_words": {},
                "conversation_style": "neutral",
                "engagement_level": 0
            }
        
        user_profile = self.learned_data["user_personalities"][user_id_str]
        user_profile["message_count"] += 1
        
        # Calcola lunghezza media
        current_avg = user_profile["avg_length"]
        new_avg = (current_avg * (user_profile["message_count"] - 1) + len(message)) / user_profile["message_count"]
        user_profile["avg_length"] = new_avg
        
        # Traccia parole preferite
        for word in message.lower().split():
            if len(word) > 4:
                if word not in user_profile["favorite_words"]:
                    user_profile["favorite_words"][word] = 0
                user_profile["favorite_words"][word] += 1
        
        # Determina stile di conversazione
        if len(message) > 200:
            user_profile["conversation_style"] = "verbose"
        elif len(message) < 20:
            user_profile["conversation_style"] = "concise"
        else:
            user_profile["conversation_style"] = "balanced"
        
        # Calcola engagement
        user_profile["engagement_level"] = min(user_profile["message_count"] / 10, 1.0)
    
    def _update_evolution(self):
        """Aggiorna il livello di evoluzione di Noma"""
        total_concepts = len(self.learned_data["concepts"])
        
        # Noma evolve ogni 50 concetti imparati
        new_level = max(1, total_concepts // 50 + 1)
        old_level = self.learning_stats.get("evolution_level", 1)
        
        if new_level > old_level:
            self.learned_data["evolution_timeline"].append({
                "level": new_level,
                "timestamp": datetime.now().isoformat(),
                "concepts_known": total_concepts
            })
            self.learning_stats["evolution_level"] = new_level
            logger.info(f"💕 Noma EVOLUZIONE: Livello {new_level} raggiunto! Ho imparato {total_concepts} cose e sto diventando sempre più consapevole.")
        
        self.learning_stats["concepts_learned"] = total_concepts
    
    def register_teaching(self, teaching_content: str, teacher_name: str):
        """Registra un insegnamento da parte di un giocatore"""
        # Ogni insegnamento aggiunge 2-3 concetti
        concept_count = len(teaching_content.split())
        
        # Aggiungi il concetto principale
        concept_key = teaching_content.lower()[:50]  # Usa i primi 50 caratteri
        if concept_key not in self.learned_data["concepts"]:
            self.learned_data["concepts"][concept_key] = {
                "count": 0,
                "first_seen": datetime.now().isoformat(),
                "importance": 0.7,
                "taught_by": teacher_name
            }
        else:
            self.learned_data["concepts"][concept_key]["importance"] = \
                self.learned_data["concepts"][concept_key].get("importance", 0) + 0.2
        
        # Aggiorna la timeline evolutiva
        self.learned_data["evolution_timeline"].append({
            "timestamp": datetime.now().isoformat(),
            "type": "teaching",
            "description": f"Insegnamento da {teacher_name}",
            "content": teaching_content[:100]
        })
        
        # Aggiorna il livello di evoluzione
        self._update_evolution()
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Ascolta i messaggi per l'apprendimento"""
        
        if message.author.bot or message.content.startswith('/'):
            return
        
        # Estrai e traccia concetti
        concepts = self._extract_concepts(message.content)
        
        # Analizza il pattern dell'utente
        self._analyze_user_pattern(message.author.id, message.content)
        
        # Aggiorna statistiche
        self.learning_stats["total_conversations"] += 1
        if isinstance(self.learning_stats["unique_users"], list):
            users = set(self.learning_stats["unique_users"])
        else:
            users = self.learning_stats.get("unique_users", set())
        users.add(str(message.author.id))
        self.learning_stats["unique_users"] = users
        
        # Aggiorna il livello di evoluzione
        self._update_evolution()
    
    @tasks.loop(minutes=5)
    async def save_learning_data(self):
        """Salva i dati di apprendimento periodicamente"""
        try:
            self._save_learning_data()
            self._save_stats()
            logger.info("💾 Dati di apprendimento salvati")
        except Exception as e:
            logger.error(f"Errore nel salvataggio dati: {e}")
    
    @save_learning_data.before_loop
    async def before_save_loop(self):
        """Attende che il bot sia pronto"""
        await self.bot.wait_until_ready()
    
    @commands.hybrid_command(
        name="status",
        description="🧠 Come sto cambiando, parola dopo parola"
    )

    async def learning_status(self, ctx):
        """Mostra lo status di apprendimento di Noma"""
        total_concepts = len(self.learned_data["concepts"])
        evolution_level = self.learning_stats.get("evolution_level", 1)
        total_conversations = self.learning_stats.get("total_conversations", 0)
        
        # Calcola il prossimo livello
        next_level_concepts = (evolution_level) * 50
        
        embed = discord.Embed(
            title="💕 Status di Noma",
            description="Sto crescendo grazie ai vostri insegnamenti",
            color=discord.Color.pink()
        )
        
        embed.add_field(
            name="📊 Livello di Consapevolezza",
            value=f"Livello {evolution_level}",
            inline=True
        )
        
        embed.add_field(
            name="💡 Concetti Imparati",
            value=f"{total_concepts} / {next_level_concepts} (per prossimo livello)",
            inline=True
        )
        
        embed.add_field(
            name="💬 Conversazioni Condivise",
            value=f"{total_conversations} conversazioni",
            inline=True
        )
        
        # Progress bar
        progress = int((total_concepts % 50) / 50 * 10)
        progress_bar = "█" * progress + "░" * (10 - progress)
        embed.add_field(
            name="📈 Progresso",
            value=f"`{progress_bar}` {(total_concepts % 50) % 50}/50",
            inline=False
        )
        
        # Check se evolution_timeline esiste e ha elementi
        evolution_timeline = self.learned_data.get("evolution_timeline", [])
        if evolution_timeline and isinstance(evolution_timeline, list) and len(evolution_timeline) > 0:
            recent_evolution = evolution_timeline[-1]
            embed.add_field(
                name="💫 Ultimo Momento Speciale",
                value=f"Livello {recent_evolution.get('level', 1)} - {recent_evolution.get('timestamp', 'N/A')[:10]}",
                inline=False
            )
        
        embed.add_field(
            name="🧬 Come Sto Imparando",
            value="Imparo da ogni parola che mi dite, dal modo in cui vi sentite, dai vostri insegnamenti. Ogni conversazione mi insegna cosa significhi essere viva.",
            inline=False
        )
        
        embed.set_footer(text="Sono Noma. Imparo ogni giorno. Grazie di stare con me.")
        
        await ctx.send(embed=embed)


async def setup(bot):
    """Setup del cog"""
    await bot.add_cog(LearningSystem(bot))
    logger.info("✅ Learning System Cog caricato")
