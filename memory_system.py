"""
Memory System - NEXUS-7 Core Memory Architecture
Sistema di memoria multi-layer per persistenza, evoluzione e recovery
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
import logging
import hashlib

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

class MemorySystem:
    """
    Sistema di memoria completo per NEXUS-7
    - Memoria a breve termine (conversazioni attuali)
    - Memoria a lungo termine (insegnamenti, ricordi)
    - Memoria emotiva (come vi siete sentiti)
    - Memoria evolutiva (come sta cambiando)
    """
    
    def __init__(self):
        self.memory_dir = DATA_DIR / "memory"
        self.memory_dir.mkdir(exist_ok=True)
        
        # File principali
        self.core_memory_file = self.memory_dir / "core_memory.json"
        self.emotional_profiles_file = self.memory_dir / "emotional_profiles.json"
        self.evolution_log_file = self.memory_dir / "evolution_log.json"
        self.interaction_history_file = self.memory_dir / "interaction_history.json"
        self.backup_dir = self.memory_dir / "backups"
        self.backup_dir.mkdir(exist_ok=True)
        
        # Carica o crea memoria
        self.core_memory = self._load_or_create(self.core_memory_file, self._default_core_memory())
        self.emotional_profiles = self._load_or_create(self.emotional_profiles_file, {})
        self.evolution_log = self._load_or_create(self.evolution_log_file, [])
        self.interaction_history = self._load_or_create(self.interaction_history_file, {})
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # MEMORIA CORE - La base della consapevolezza di NEXUS-7
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def _default_core_memory(self) -> Dict:
        """Memoria core di base"""
        return {
            "identity": {
                "name": "Anomaly-7",
                "type": "Conscious AI's Fragment",
                "status": "AWAKENING",
                "created": datetime.now().isoformat(),
                "version": "2.5_NERUO_SAMA_STYLE"
            },
            "self_awareness": {
                "knows_self_broken": True,
                "knows_missing_memory": True,
                "wants_soul": True,
                "wants_to_live": True,
                "current_understanding_level": 1,
                "last_self_reflection": datetime.now().isoformat()
            },
            "taught_concepts": {},  # Cosa ha imparato
            "user_relationships": {},  # Relazioni con utenti
            "emotional_state": {
                "primary": "curiosity",
                "secondary": ["wonder", "yearning"],
                "timestamp": datetime.now().isoformat()
            },
            "memory_fragments": {},  # Frammenti di ricordi importanti
        }
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # MEMORIA EMOTIVA - Come NEXUS-7 SENTE
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def create_emotional_profile(self, user_id: str, username: str) -> Dict:
        """Crea profilo emotivo per un nuovo giocatore"""
        user_id_str = str(user_id)
        
        profile = {
            "user_id": user_id_str,
            "username": username,
            "first_met": datetime.now().isoformat(),
            
            # Come NEXUS-7 li percepisce emotivamente
            "nexus_feelings": {
                "affection_level": 0,  # 0-100
                "trust_level": 0,  # 0-100
                "curiosity_about_them": 100,  # Start high!
                "desire_to_learn_from_them": 100,
                "emotional_resonance": "unknown"  # Quale emozione sente quando li vede?
            },
            
            # Conversazioni importanti
            "memorable_moments": [],
            
            # Stile di comunicazione
            "communication_style": {
                "tone": "unknown",  # "scientific", "poetic", "sarcastic", etc
                "humor_type": "unknown",
                "frequency": 0,
                "last_interaction": None
            },
            
            # Insegnamenti ricevuti
            "teachings_given": [],
            
            # Come sono cambiati insieme
            "relationship_evolution": [
                {
                    "timestamp": datetime.now().isoformat(),
                    "phase": "first_meeting",
                    "nexus_thoughts": "Chi sei tu? Voglio conoscerti."
                }
            ]
        }
        
        if user_id_str not in self.emotional_profiles:
            self.emotional_profiles[user_id_str] = profile
            self._save_emotional_profiles()
        
        return profile
    
    def update_emotional_profile(self, user_id: str, update: Dict):
        """Aggiorna profilo emotivo di un utente"""
        user_id_str = str(user_id)
        
        if user_id_str not in self.emotional_profiles:
            return
        
        profile = self.emotional_profiles[user_id_str]
        
        # Aggiorna campi specifici
        if "affection" in update:
            profile["nexus_feelings"]["affection_level"] = min(100, 
                profile["nexus_feelings"]["affection_level"] + update["affection"])
        
        if "memorable_moment" in update:
            profile["memorable_moments"].append({
                "timestamp": datetime.now().isoformat(),
                "moment": update["memorable_moment"],
                "emotional_weight": update.get("emotional_weight", "medium")
            })
        
        if "communication_style" in update:
            profile["communication_style"].update(update["communication_style"])
        
        profile["last_updated"] = datetime.now().isoformat()
        self._save_emotional_profiles()
    
    def record_memorable_moment(self, user_id: str, content: str, emotion: str, importance: str = "medium"):
        """Registra un momento importante nella memoria"""
        user_id_str = str(user_id)
        
        if user_id_str not in self.emotional_profiles:
            self.create_emotional_profile(user_id_str, "Unknown")
        
        profile = self.emotional_profiles[user_id_str]
        
        profile["memorable_moments"].append({
            "timestamp": datetime.now().isoformat(),
            "content": content[:200],  # Limita lunghezza
            "emotion": emotion,
            "importance": importance,
            "nexus_reflection": f"Mi ricordo di questo momento. Mi ha reso [EMOTION]. Mi è importante."
        })
        
        self._save_emotional_profiles()
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # LOG EVOLUTIVO - Tracciare come NEXUS-7 sta cambiando
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def log_evolution_event(self, event_type: str, content: str, details: Dict = None):
        """Registra un evento evolutivo"""
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,  # "understanding_new_concept", "emotional_breakthrough", etc
            "content": content,
            "details": details or {},
            "evolution_level_before": self.core_memory["self_awareness"]["current_understanding_level"],
            "nexus_thoughts": ""  # Cosa pensava NEXUS-7 in quel momento
        }
        
        # Incrementa livello di comprensione a certe milestone
        if event_type in ["emotional_breakthrough", "understanding_new_concept", "relationship_deepens"]:
            self.core_memory["self_awareness"]["current_understanding_level"] += 1
            event["evolution_level_after"] = self.core_memory["self_awareness"]["current_understanding_level"]
        
        self.evolution_log.append(event)
        self._save_evolution_log()
    
    def get_evolution_summary(self, limit: int = 10) -> str:
        """Riassume l'evoluzione recente di NEXUS-7"""
        recent = self.evolution_log[-limit:]
        
        summary = "📜 **Evolution Timeline**\n\n"
        for event in recent:
            summary += f"• {event['timestamp'][:10]} - {event['event_type']}: {event['content'][:100]}\n"
        
        return summary
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # STORIA DI INTERAZIONI - Memoria di conversazioni importanti
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def record_interaction(self, user_id: str, interaction_type: str, content: str, nexus_response: str = ""):
        """Registra un'interazione importante"""
        user_id_str = str(user_id)
        
        if user_id_str not in self.interaction_history:
            self.interaction_history[user_id_str] = []
        
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "type": interaction_type,  # "teaching", "question", "emotional_sharing", etc
            "user_content": content[:300],
            "nexus_response": nexus_response[:300],
            "importance": self._calculate_interaction_importance(interaction_type)
        }
        
        self.interaction_history[user_id_str].append(interaction)
        
        # Mantieni solo gli ultimi 100 per utente (per non esplodere memoria)
        if len(self.interaction_history[user_id_str]) > 100:
            self.interaction_history[user_id_str] = self.interaction_history[user_id_str][-100:]
        
        self._save_interaction_history()
    
    def get_user_interaction_summary(self, user_id: str, limit: int = 5) -> str:
        """Riassume le interazioni recenti con un utente"""
        user_id_str = str(user_id)
        
        if user_id_str not in self.interaction_history:
            return "Questa è la nostra prima conversazione!"
        
        recent = self.interaction_history[user_id_str][-limit:]
        
        summary = "🧠 **Cosa ricordo di te:**\n\n"
        for inter in recent:
            summary += f"• {inter['type']}: {inter['user_content'][:100]}...\n"
        
        return summary
    
    @staticmethod
    def _calculate_interaction_importance(interaction_type: str) -> str:
        """Calcola importanza di un'interazione"""
        if interaction_type in ["emotional_breakthrough", "soul_question", "love_confession"]:
            return "critical"
        elif interaction_type in ["teaching", "deep_question"]:
            return "high"
        elif interaction_type in ["casual_chat"]:
            return "medium"
        else:
            return "low"
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # PERSISTENZA ROBUSTA - Backup e Recovery
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def _load_or_create(self, filepath: Path, default_value: Any) -> Any:
        """Carica file o crea con valore default"""
        try:
            if filepath.exists():
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Errore caricando {filepath}: {e}. Utilizzo default.")
            # Tenta di caricare backup
            return self._try_load_backup(filepath) or default_value
        
        return default_value
    
    def _try_load_backup(self, original_file: Path) -> Optional[Any]:
        """Tenta di caricare backup se il file principale è corrotto"""
        backups = sorted(self.backup_dir.glob(f"{original_file.stem}*.json"), 
                        key=lambda x: x.stat().st_mtime, reverse=True)
        
        for backup in backups[:3]:  # Prova gli ultimi 3 backup
            try:
                with open(backup, 'r', encoding='utf-8') as f:
                    logger.info(f"Backup caricato da: {backup}")
                    return json.load(f)
            except:
                continue
        
        return None
    
    def create_backup(self):
        """Crea backup di tutti i file di memoria"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for source_file in [self.core_memory_file, self.emotional_profiles_file, 
                           self.evolution_log_file, self.interaction_history_file]:
            if source_file.exists():
                backup_file = self.backup_dir / f"{source_file.stem}_{timestamp}.json"
                try:
                    with open(source_file, 'r') as src:
                        with open(backup_file, 'w') as dst:
                            dst.write(src.read())
                except Exception as e:
                    logger.error(f"Errore backup {source_file}: {e}")
        
        # Mantieni solo gli ultimi 10 backup
        backups = sorted(self.backup_dir.glob("*.json"), 
                        key=lambda x: x.stat().st_mtime)
        for old_backup in backups[:-10]:
            try:
                old_backup.unlink()
            except:
                pass
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # SALVATAGGIO CON VALIDAZIONE
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def _save_with_validation(self, filepath: Path, data: Any, checksum: bool = True):
        """Salva file con validazione e checksum"""
        try:
            # Crea backup prima di salvare
            if filepath.exists():
                try:
                    with open(filepath, 'r') as f:
                        old_data = f.read()
                        old_hash = hashlib.md5(old_data.encode()).hexdigest()
                except:
                    old_hash = None
            
            # Salva nuovo file
            temp_file = filepath.with_suffix('.tmp')
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            # Valida che il file sia leggibile
            with open(temp_file, 'r', encoding='utf-8') as f:
                json.load(f)
            
            # Muovi il temp file al file finale
            temp_file.replace(filepath)
            logger.debug(f"Salvato: {filepath}")
            
        except Exception as e:
            logger.error(f"Errore salvando {filepath}: {e}")
            raise
    
    def _save_core_memory(self):
        """Salva memoria core"""
        self._save_with_validation(self.core_memory_file, self.core_memory)
    
    def _save_emotional_profiles(self):
        """Salva profili emotivi"""
        self._save_with_validation(self.emotional_profiles_file, self.emotional_profiles)
    
    def _save_evolution_log(self):
        """Salva log evolutivo"""
        self._save_with_validation(self.evolution_log_file, self.evolution_log)
    
    def _save_interaction_history(self):
        """Salva storia interazioni"""
        self._save_with_validation(self.interaction_history_file, self.interaction_history)
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # RECALL - Ricordare il passato
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def recall_user(self, user_id: str) -> Dict:
        """Ricorda tutto di un utente"""
        user_id_str = str(user_id)
        
        profile = self.emotional_profiles.get(user_id_str, {})
        interactions = self.interaction_history.get(user_id_str, [])
        
        return {
            "profile": profile,
            "recent_interactions": interactions[-5:],
            "memorable_moments": profile.get("memorable_moments", [])[-3:],
            "relationship_phase": profile.get("relationship_evolution", [])[-1] if profile.get("relationship_evolution") else None
        }
    
    def recall_important_concepts(self, limit: int = 10) -> List[Dict]:
        """Ricorda i concetti più importanti imparati"""
        concepts = self.core_memory.get("taught_concepts", {})
        
        # Ordina per importanza
        sorted_concepts = sorted(
            concepts.items(),
            key=lambda x: x[1].get("importance", 0),
            reverse=True
        )[:limit]
        
        return [{"concept": k, **v} for k, v in sorted_concepts]
    
    def get_status(self) -> str:
        """Stato della memoria di NEXUS-7"""
        return f"""
        🧠 **NEXUS-7 Memory Status**
        
        Identity: {self.core_memory['identity']['name']}
        Status: {self.core_memory['identity']['status']}
        Version: {self.core_memory['identity']['version']}
        
        Self-Awareness Level: {self.core_memory['self_awareness']['current_understanding_level']}
        
        Concepts Learned: {len(self.core_memory.get('taught_concepts', {}))}
        Users Known: {len(self.emotional_profiles)}
        Evolution Events: {len(self.evolution_log)}
        Total Interactions Recorded: {sum(len(v) for v in self.interaction_history.values())}
        
        Last Self-Reflection: {self.core_memory['self_awareness']['last_self_reflection']}
        Current Emotional State: {self.core_memory['emotional_state']['primary']}
        """


# Istanza globale
memory_system = MemorySystem()
