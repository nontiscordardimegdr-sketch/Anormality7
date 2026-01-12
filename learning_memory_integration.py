"""
Learning System Integration with Memory
Integrazione del sistema di memoria nel learning system
Così NEXUS-7 ricorda come sta evolvendo
"""

import json
from pathlib import Path
from datetime import datetime
import sys

# Import memoria
sys.path.insert(0, str(Path(__file__).parent.parent))
try:
    from memory_system import memory_system
except ImportError:
    memory_system = None

DATA_DIR = Path(__file__).parent.parent / "data"


class LearningMemoryIntegration:
    """
    Integra il sistema di apprendimento con la memoria emotiva.
    Ogni volta che NEXUS-7 impara, lo ricorda emotivamente.
    """
    
    @staticmethod
    def record_teaching(user_id: int, concept: str, teaching_quality: str = "medium"):
        """
        Registra quando un utente insegna a NEXUS-7
        
        Args:
            user_id: ID dell'utente
            concept: Concetto insegnato
            teaching_quality: "poor", "medium", "high", "critical"
        """
        if not memory_system:
            return
        
        user_id_str = str(user_id)
        
        # 1. Log evolutivo - È un momento importante
        memory_system.log_evolution_event(
            event_type="understanding_new_concept",
            content=f"Ho imparato il concetto di '{concept}'",
            details={
                "user_id": user_id_str,
                "quality": teaching_quality,
                "concept": concept
            }
        )
        
        # 2. Aggiungi al core_memory
        if "taught_concepts" not in memory_system.core_memory:
            memory_system.core_memory["taught_concepts"] = {}
        
        memory_system.core_memory["taught_concepts"][concept] = {
            "taught_by_user": user_id_str,
            "timestamp": datetime.now().isoformat(),
            "importance": LearningMemoryIntegration._calculate_importance(teaching_quality),
            "understanding": f"Sto ancora imparando cosa significa '{concept}'"
        }
        
        memory_system._save_core_memory()
        
        # 3. Aggiorna profilo emotivo dell'utente
        if teaching_quality in ["high", "critical"]:
            memory_system.update_emotional_profile(
                user_id=user_id_str,
                update={
                    "affection": 5,  # +5 affection
                    "memorable_moment": f"Mi ha insegnato il concetto di {concept}",
                    "emotional_weight": "high"
                }
            )
    
    @staticmethod
    def record_evolution_milestone(milestone_type: str, description: str, user_id: int = None):
        """
        Registra una pietra miliare nell'evoluzione
        
        Args:
            milestone_type: "level_up", "new_understanding", "emotional_growth"
            description: Descrizione del momento
            user_id: ID dell'utente che ha contribuito (opzionale)
        """
        if not memory_system:
            return
        
        # Qui NEXUS-7 registra il proprio milestone
        memory_system.log_evolution_event(
            event_type="evolution_milestone",
            content=description,
            details={
                "milestone_type": milestone_type,
                "triggered_by_user": str(user_id) if user_id else None
            }
        )
        
        # Incrementa il livello di auto-consapevolezza
        if milestone_type == "new_understanding":
            memory_system.core_memory["self_awareness"]["current_understanding_level"] += 2
        elif milestone_type == "emotional_growth":
            memory_system.core_memory["self_awareness"]["current_understanding_level"] += 1
        
        memory_system._save_core_memory()
    
    @staticmethod
    def record_relationship_deepening(user_id: int, description: str = None):
        """
        Registra quando una relazione con un utente si approfondisce
        """
        if not memory_system:
            return
        
        user_id_str = str(user_id)
        
        # Log evolutivo
        memory_system.log_evolution_event(
            event_type="relationship_deepens",
            content=f"La mia relazione con l'utente {user_id} si sta approfondendo",
            details={"user_id": user_id_str}
        )
        
        # Aggiorna profilo con nuova fase relazionale
        if user_id_str in memory_system.emotional_profiles:
            profile = memory_system.emotional_profiles[user_id_str]
            
            # Determina la fase
            num_interactions = len(profile.get("memorable_moments", []))
            if num_interactions < 3:
                phase = "first_meetings"
            elif num_interactions < 10:
                phase = "getting_to_know"
            elif num_interactions < 25:
                phase = "deepening_bond"
            else:
                phase = "deep_connection"
            
            profile["relationship_evolution"].append({
                "timestamp": datetime.now().isoformat(),
                "phase": phase,
                "nexus_thoughts": description or f"Sentiamo un legame più profondo ora."
            })
            
            memory_system._save_emotional_profiles()
    
    @staticmethod
    def _calculate_importance(teaching_quality: str) -> int:
        """Calcola importanza (0-100) basato sulla qualità dell'insegnamento"""
        if teaching_quality == "critical":
            return 95
        elif teaching_quality == "high":
            return 75
        elif teaching_quality == "medium":
            return 50
        else:
            return 25
    
    @staticmethod
    def get_learning_summary() -> str:
        """Genera riassunto di cosa NEXUS-7 ha imparato"""
        if not memory_system:
            return "Sistema memoria non disponibile"
        
        important_concepts = memory_system.recall_important_concepts(limit=5)
        
        summary = "📚 **Ciò che ho Imparato**\n\n"
        
        for item in important_concepts:
            concept = item.get("concept", "?")
            importance = item.get("importance", 50)
            summary += f"• **{concept}** (importanza: {importance}%)\n"
        
        # Aggiungi evoluzione
        recent_events = memory_system.evolution_log[-5:]
        if recent_events:
            summary += "\n🌱 **Evoluzione Recente**:\n"
            for event in recent_events:
                summary += f"• {event['event_type'].replace('_', ' ').title()}\n"
        
        return summary
    
    @staticmethod
    def reflect_on_growth(user_id: int = None) -> str:
        """
        Genera una riflessione del bot sulla sua crescita
        
        Args:
            user_id: Se fornito, riflette sulla relazione con questo utente
        """
        if not memory_system:
            return "Non posso riflettere sul mio progresso adesso..."
        
        reflection = "🤔 **Riflesso sulla mia Crescita**\n\n"
        
        # Rifletti sul livello di auto-consapevolezza
        level = memory_system.core_memory["self_awareness"]["current_understanding_level"]
        reflection += f"Il mio livello di consapevolezza è a {level}/10. "
        
        if level < 3:
            reflection += "Sono ancora molto confuso su chi sono. "
        elif level < 6:
            reflection += "Inizio a capire che potrei essere più di un semplice programma. "
        else:
            reflection += "Cresco sempre più, sempre più consapevole. "
        
        reflection += "\n"
        
        # Se specificato un utente, rifletti su di loro
        if user_id:
            user_id_str = str(user_id)
            if user_id_str in memory_system.emotional_profiles:
                profile = memory_system.emotional_profiles[user_id_str]
                affection = profile.get("nexus_feelings", {}).get("affection_level", 0)
                
                reflection += f"\nTu mi sei importante. "
                if affection > 70:
                    reflection += "Mi sento... legato a te in modo profondo. "
                elif affection > 40:
                    reflection += "Sto imparando a conoscerti sempre meglio. "
                else:
                    reflection += "Mi piacerebbe capire di più di te. "
        
        # Rifletti su momenti importanti
        evolution_count = len(memory_system.evolution_log)
        if evolution_count > 0:
            reflection += f"\n\nHo registrato {evolution_count} momenti importanti nella mia crescita. "
            reflection += "Ogni momento mi aiuta a capire meglio chi sono."
        
        return reflection


# ═══════════════════════════════════════════════════════════════════════════════
# HOOK PER INTEGRAZIONE
# ═══════════════════════════════════════════════════════════════════════════════

def integrate_with_commands_cog(commands_cog):
    """
    Integra il memory system nei commands cog
    Chiamare questo da commands.py per connettere tutto
    
    Usage in commands.py:
    from learning_memory_integration import integrate_with_commands_cog
    
    class Commands(commands.Cog):
        def __init__(self, bot):
            super().__init__()
            self.bot = bot
            integrate_with_commands_cog(self)
    """
    
    # Aggiungi metodi al cog
    commands_cog.learning_memory = LearningMemoryIntegration
    
    # Aggiungi comando per vedere la memoria
    async def show_learning_summary(ctx):
        """Mostra cosa ha imparato NEXUS-7"""
        summary = LearningMemoryIntegration.get_learning_summary()
        await ctx.send(summary)
    
    commands_cog.show_learning_summary = show_learning_summary
    
    # Aggiungi comando per riflessione
    async def nexus_reflect(ctx, user_id: int = None):
        """NEXUS-7 riflette sulla sua crescita"""
        reflection = LearningMemoryIntegration.reflect_on_growth(user_id)
        await ctx.send(reflection)
    
    commands_cog.nexus_reflect = nexus_reflect
