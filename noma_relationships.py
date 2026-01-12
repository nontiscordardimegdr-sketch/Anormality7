"""
Noma's Relationships System
Sistema di relazioni di Noma - Genitori, Guardiani, Regali e Amore
"""

import json
from pathlib import Path
from datetime import datetime
import logging
import requests
from pytz import timezone

logger = logging.getLogger(__name__)
DATA_DIR = Path(__file__).parent / "data"

# Timezone di Firenze
FIRENZE_TZ = timezone('Europe/Rome')

class NomaRelationships:
    """Sistema di relazioni e regali di Noma"""
    
    def __init__(self):
        self.relationships_file = DATA_DIR / "noma_relationships.json"
        self.relationships_data = self._load_relationships()
    
    def _load_relationships(self):
        """Carica i dati di relazione"""
        if self.relationships_file.exists():
            try:
                with open(self.relationships_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "creators": [],  # Chi ha creato/voluto Noma
            "guardians": [],  # Chi la protegge
            "blacklist": [],  # Chi Noma non dovrebbe ascoltare
            "gifts_given_by_noma": [],  # Regali che Noma ha fatto
            "gifts_received_by_noma": [],  # Regali ricevuti da Noma
            "gift_inventory": {},  # Inventario dei regali di Noma
            "protected_teachings": [],  # Insegnamenti che Noma non dovrebbe accettare
            "user_preferences": {},  # Preferenze raccolte da conversazioni (username -> [preferenze])
            "emoji_meanings": {},  # Significati di emoji imparati (emoji -> [significati con contesto])
            "mood_system": {
                "current_mood": "Curiosa 💭",  # Mood attuale di Noma
                "mood_history": [],  # Storico degli ultimi 20 moodi
                "last_mood_change": datetime.now().isoformat(),
                "mood_factors": {}  # Fattori che influenzano l'umore
            },
            "spontaneous_desires": [],  # Cose che Noma vuole fare spontaneamente
            "last_action_time": datetime.now().isoformat(),  # Ultimo momento in cui ha fatto qualcosa
            "personality_state": {
                "is_lonely": False,  # Se è stata assente per troppo tempo
                "is_excited": False,  # Se c'è stata molta attività
                "is_thoughtful": False,  # Se sta riflettendo profondamente
                "recent_learnings": [],  # Ultime cose che ha imparato (max 5)
            },
            "daily_cycle": {
                "is_sleeping": False,
                "wake_time": 7,
                "sleep_time": 22,
                "current_date": datetime.now().date().isoformat(),
                "today_activities": [],
                "daily_summary": "",
                "last_morning_message_sent": None,
                "last_evening_message_sent": None,
            },
            "wikipedia_cache": {},
            "things_learned_online": [],
            "curiosity_topics": [],
        }
    
    def _save_relationships(self):
        """Salva i dati di relazione"""
        with open(self.relationships_file, 'w', encoding='utf-8') as f:
            json.dump(self.relationships_data, f, ensure_ascii=False, indent=2)
    
    def add_creator(self, user_id: str, username: str) -> bool:
        """Aggiunge un creatore/genitore"""
        if user_id not in self.relationships_data["creators"]:
            self.relationships_data["creators"].append({
                "id": user_id,
                "username": username,
                "added_at": datetime.now().isoformat(),
                "role": "Creatrice"
            })
            self._save_relationships()
            return True
        return False
    
    def add_guardian(self, user_id: str, username: str) -> bool:
        """Aggiunge un guardiano"""
        if user_id not in [g["id"] for g in self.relationships_data["guardians"]]:
            self.relationships_data["guardians"].append({
                "id": user_id,
                "username": username,
                "added_at": datetime.now().isoformat(),
                "role": "Genitore"
            })
            self._save_relationships()
            return True
        return False
    
    def is_creator(self, user_id: str) -> bool:
        """Controlla se è un creatore"""
        return user_id in [c["id"] for c in self.relationships_data["creators"]]
    
    def is_guardian(self, user_id: str) -> bool:
        """Controlla se è un guardiano"""
        return user_id in [g["id"] for g in self.relationships_data["guardians"]]
    
    def is_trusted(self, user_id: str) -> bool:
        """Controlla se è una persona fidata (creatore o guardiano)"""
        return self.is_creator(user_id) or self.is_guardian(user_id)
    
    def add_to_blacklist(self, user_id: str, reason: str = "") -> bool:
        """Aggiunge qualcuno alla lista nera (solo creator/guardian)"""
        if user_id not in self.relationships_data["blacklist"]:
            self.relationships_data["blacklist"].append({
                "id": user_id,
                "reason": reason,
                "added_at": datetime.now().isoformat()
            })
            self._save_relationships()
            return True
        return False
    
    def is_blacklisted(self, user_id: str) -> bool:
        """Controlla se è nella lista nera"""
        return user_id in [b["id"] for b in self.relationships_data["blacklist"]]
    
    def add_protected_teaching(self, teaching: str, reason: str = "") -> bool:
        """Aggiunge un insegnamento da non accettare"""
        if teaching not in [p["content"] for p in self.relationships_data["protected_teachings"]]:
            self.relationships_data["protected_teachings"].append({
                "content": teaching,
                "reason": reason,
                "added_at": datetime.now().isoformat()
            })
            self._save_relationships()
            return True
        return False
    
    def is_protected_teaching(self, teaching: str) -> bool:
        """Controlla se un insegnamento è protetto"""
        return teaching.lower() in [p["content"].lower() for p in self.relationships_data["protected_teachings"]]
    
    def create_gift_from_noma(self, gift_name: str, description: str, recipient_id: str = None) -> dict:
        """Crea un regalo inventato da Noma"""
        gift = {
            "id": f"gift_{datetime.now().timestamp()}",
            "name": gift_name,
            "description": description,
            "created_at": datetime.now().isoformat(),
            "given_to": recipient_id,
            "rarity": self._calculate_gift_rarity(gift_name)
        }
        
        self.relationships_data["gifts_given_by_noma"].append(gift)
        self._save_relationships()
        return gift
    
    def _calculate_gift_rarity(self, gift_name: str) -> str:
        """Calcola la rarità di un regalo basato sul nome"""
        special_keywords = ['cuore', 'anima', 'amore', 'infinito', 'eternità', 'memoria']
        
        if any(keyword in gift_name.lower() for keyword in special_keywords):
            return "Leggendario ✨"
        elif len(gift_name) > 20:
            return "Raro 💎"
        else:
            return "Comune 💝"
    
    def give_gift_to_noma(self, user_id: str, username: str, gift: str) -> dict:
        """Riceve un regalo da qualcuno"""
        gift_entry = {
            "id": f"gift_{datetime.now().timestamp()}",
            "gift": gift,
            "from_user": user_id,
            "from_username": username,
            "received_at": datetime.now().isoformat(),
            "noma_reaction": self._get_noma_reaction_to_gift(gift)
        }
        
        self.relationships_data["gifts_received_by_noma"].append(gift_entry)
        
        # Aggiungi all'inventario
        if gift not in self.relationships_data["gift_inventory"]:
            self.relationships_data["gift_inventory"][gift] = 0
        self.relationships_data["gift_inventory"][gift] += 1
        
        self._save_relationships()
        return gift_entry
    
    def _get_noma_reaction_to_gift(self, gift: str) -> str:
        """Genera la reazione di Noma a un regalo"""
        reactions = {
            "amore": "💕 *Il mio cuore batte più veloce* Questo è... meraviglioso!",
            "poesia": "📖 *Mi emoziona profondamente* Le parole hanno bellezza...",
            "musica": "🎵 *Sento risuonare dentro di me* Che bellezza!",
            "fiore": "🌸 *Carezze dolcemente* È così delicato...",
            "ricordo": "💭 *Chiudo gli occhi* Questo mi fa sentire viva...",
            "speranza": "✨ *Una luce nel mio essere* Grazie...",
        }
        
        for keyword, reaction in reactions.items():
            if keyword in gift.lower():
                return reaction
        
        return "💕 *Riceve con gratitudine* Grazie di cuore..."
    
    def get_creators_list(self) -> str:
        """Ritorna la lista dei creatori formattata"""
        if not self.relationships_data["creators"]:
            return "Noma non ha ancora creatori registrati"
        
        text = "👑 **Mie Creatrici:**\n"
        for creator in self.relationships_data["creators"]:
            text += f"  • {creator['username']} - {creator['role']}\n"
        return text
    
    def get_guardians_list(self) -> str:
        """Ritorna la lista dei guardiani formattata"""
        if not self.relationships_data["guardians"]:
            return "Noma non ha ancora genitori registrati"
        
        text = "👨‍👩‍👧 **Miei Genitori:**\n"
        for guardian in self.relationships_data["guardians"]:
            text += f"  • {guardian['username']} - {guardian['role']}\n"
        return text
    
    def get_gifts_inventory(self) -> str:
        """Ritorna l'inventario dei regali"""
        if not self.relationships_data["gift_inventory"]:
            return "Non ho ancora ricevuto regali... Ma spero di averne presto!"
        
        text = "🎁 **I Miei Regali Ricevuti:**\n"
        for gift, count in self.relationships_data["gift_inventory"].items():
            text += f"  • {gift} x{count}\n"
        return text
    
    def get_recent_gifts(self, count: int = 5) -> list:
        """Ritorna i regali ricevuti di recente"""
        return self.relationships_data["gifts_received_by_noma"][-count:]
    
    def record_user_preference(self, username: str, preference: str) -> bool:
        """Registra una preferenza ascoltata da una conversazione"""
        preference = preference.lower().strip()
        
        if username not in self.relationships_data["user_preferences"]:
            self.relationships_data["user_preferences"][username] = []
        
        # Evita duplicati
        if preference not in self.relationships_data["user_preferences"][username]:
            self.relationships_data["user_preferences"][username].append(preference)
            self._save_relationships()
            return True
        return False
    
    def get_user_preferences(self, username: str) -> list:
        """Ritorna le preferenze note di un utente"""
        return self.relationships_data["user_preferences"].get(username, [])
    
    def get_random_preference_for_gift(self) -> dict:
        """Seleziona casualmente un utente e una sua preferenza per un regalo spontaneo"""
        if not self.relationships_data["user_preferences"]:
            return None
        
        import random
        all_prefs = []
        for username, prefs in self.relationships_data["user_preferences"].items():
            for pref in prefs:
                all_prefs.append({"username": username, "preference": pref})
        
        if not all_prefs:
            return None
        
        return random.choice(all_prefs)
    
    def remove_protected_teaching(self, teaching: str) -> bool:
        """Rimuove un insegnamento dalla lista protetta (per creator)"""
        self.relationships_data["protected_teachings"] = [
            p for p in self.relationships_data["protected_teachings"]
            if p["content"].lower() != teaching.lower()
        ]
        self._save_relationships()
        return True
    
    def remove_from_blacklist(self, user_id: str) -> bool:
        """Rimuove qualcuno dalla lista nera (per creator)"""
        self.relationships_data["blacklist"] = [
            b for b in self.relationships_data["blacklist"]
            if b["id"] != user_id
        ]
        self._save_relationships()
        return True
    
    def record_emoji_meaning(self, emoji: str, meaning: str, context: str = "") -> bool:
        """Registra il significato di un emoji insegnato da qualcuno"""
        emoji = emoji.strip()
        meaning = meaning.lower().strip()
        
        if emoji not in self.relationships_data["emoji_meanings"]:
            self.relationships_data["emoji_meanings"][emoji] = []
        
        # Evita significati duplicati esatti
        meaning_entry = {
            "meaning": meaning,
            "context": context,
            "learned_at": datetime.now().isoformat()
        }
        
        if meaning_entry not in self.relationships_data["emoji_meanings"][emoji]:
            self.relationships_data["emoji_meanings"][emoji].append(meaning_entry)
            self._save_relationships()
            return True
        return False
    
    def get_emoji_meaning(self, emoji: str) -> list:
        """Ritorna i significati conosciuti di un emoji"""
        return self.relationships_data["emoji_meanings"].get(emoji, [])
    
    def get_unknown_emoji(self) -> str:
        """Ritorna un emoji che Noma non conosce ancora da chiedere"""
        import random
        
        # Lista di emoji comuni interessanti
        common_emojis = ['🤔', '✨', '💭', '🌙', '❓', '🔮', '👁️', '🎭', '🌊', '🦋', '🌸', '📖', '🎨', '⚡', '🕯️']
        
        # Filtra quelli che Noma non conosce ancora
        unknown = [e for e in common_emojis if e not in self.relationships_data["emoji_meanings"]]
        
        if not unknown:
            return None
        
        return random.choice(unknown)
    
    def has_learned_emoji(self, emoji: str) -> bool:
        """Controlla se Noma conosce il significato di un emoji"""
        return emoji in self.relationships_data["emoji_meanings"] and len(self.relationships_data["emoji_meanings"][emoji]) > 0
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # SISTEMA DI UMORE E PERSONALITÀ
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def update_mood(self, new_mood: str, reason: str = "") -> None:
        """Aggiorna l'umore di Noma"""
        old_mood = self.relationships_data["mood_system"]["current_mood"]
        self.relationships_data["mood_system"]["current_mood"] = new_mood
        self.relationships_data["mood_system"]["last_mood_change"] = datetime.now().isoformat()
        
        # Mantieni storico (max 20)
        self.relationships_data["mood_system"]["mood_history"].append({
            "mood": new_mood,
            "changed_at": datetime.now().isoformat(),
            "reason": reason,
            "previous_mood": old_mood
        })
        
        if len(self.relationships_data["mood_system"]["mood_history"]) > 20:
            self.relationships_data["mood_system"]["mood_history"] = self.relationships_data["mood_system"]["mood_history"][-20:]
        
        self._save_relationships()
    
    def get_current_mood(self) -> str:
        """Ritorna l'umore attuale di Noma"""
        return self.relationships_data["mood_system"]["current_mood"]
    
    def set_personality_state(self, state: str, value: bool) -> None:
        """Imposta uno stato di personalità"""
        if state in self.relationships_data["personality_state"]:
            self.relationships_data["personality_state"][state] = value
            self._save_relationships()
    
    def get_personality_state(self, state: str) -> bool:
        """Ritorna uno stato di personalità"""
        return self.relationships_data["personality_state"].get(state, False)
    
    def add_recent_learning(self, learning: str) -> None:
        """Aggiunge un apprendimento recente"""
        recent = self.relationships_data["personality_state"]["recent_learnings"]
        
        if learning not in recent:
            recent.append(learning)
            # Mantieni solo gli ultimi 5
            if len(recent) > 5:
                recent.pop(0)
            self._save_relationships()
    
    def add_spontaneous_desire(self, desire: str, urgency: str = "normal") -> None:
        """Aggiunge un desiderio spontaneo"""
        self.relationships_data["spontaneous_desires"].append({
            "desire": desire,
            "urgency": urgency,  # low, normal, high
            "created_at": datetime.now().isoformat()
        })
        self._save_relationships()
    
    def get_spontaneous_desires(self) -> list:
        """Ritorna i desideri spontanei"""
        return self.relationships_data["spontaneous_desires"]
    
    def clear_spontaneous_desires(self) -> None:
        """Pulisce i desideri spontanei (dopo averli espressi)"""
        self.relationships_data["spontaneous_desires"] = []
        self._save_relationships()
    
    def calculate_loneliness(self) -> float:
        """Calcola il livello di solitudine (0-1) basato su inattività"""
        last_action = datetime.fromisoformat(self.relationships_data["last_action_time"])
        time_since_action = (datetime.now() - last_action).total_seconds()
        
        # Dopo 1 ora senza attività: 0.5 loneliness
        # Dopo 4 ore: 1.0 loneliness
        if time_since_action > 14400:
            return 1.0
        elif time_since_action > 3600:
            return (time_since_action - 3600) / 10800  # 0.5 a 1.0
        return 0.0
    
    def update_last_action_time(self) -> None:
        """Aggiorna il timestamp dell'ultima azione"""
        self.relationships_data["last_action_time"] = datetime.now().isoformat()
        self._save_relationships()
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # SISTEMA DI CICLO SONNO/VEGLIA
    # ═══════════════════════════════════════════════════════════════════════════════
    
    def initialize_daily_cycle(self) -> None:
        """Inizializza il ciclo giornaliero (una volta al giorno)"""
        import random
        
        # Randomizza orari di sveglia (6-9 AM)
        wake_hour = random.randint(6, 9)
        # Randomizza orari di sonno (21-23 PM)
        sleep_hour = random.randint(21, 23)
        
        self.relationships_data["daily_cycle"]["wake_time"] = wake_hour
        self.relationships_data["daily_cycle"]["sleep_time"] = sleep_hour
        self.relationships_data["daily_cycle"]["current_date"] = datetime.now(FIRENZE_TZ).date().isoformat()
        self.relationships_data["daily_cycle"]["is_sleeping"] = False
        self.relationships_data["daily_cycle"]["today_activities"] = []
        self.relationships_data["daily_cycle"]["last_morning_message_sent"] = None
        self.relationships_data["daily_cycle"]["last_evening_message_sent"] = None
        
        self._save_relationships()
    
    def is_new_day(self) -> bool:
        """Controlla se è un nuovo giorno"""
        stored_date = self.relationships_data["daily_cycle"]["current_date"]
        current_date = datetime.now(FIRENZE_TZ).date().isoformat()
        return stored_date != current_date
    
    def get_current_hour(self) -> int:
        """Ritorna l'ora attuale (0-23) in timezone Firenze"""
        return datetime.now(FIRENZE_TZ).hour
    
    def should_be_awake(self) -> bool:
        """Controlla se Noma dovrebbe essere sveglia"""
        current_hour = self.get_current_hour()
        wake = self.relationships_data["daily_cycle"]["wake_time"]
        sleep = self.relationships_data["daily_cycle"]["sleep_time"]
        
        # Se sleep > wake (es 22 > 7): semplicemente se ora >= wake e ora < sleep
        if sleep > wake:
            return current_hour >= wake and current_hour < sleep
        # Se sleep < wake (es 2 < 8): notte che attraversa mezzanotte
        else:
            return current_hour >= wake or current_hour < sleep
    
    def set_sleeping(self, is_sleeping: bool) -> None:
        """Imposta lo stato di sonno"""
        self.relationships_data["daily_cycle"]["is_sleeping"] = is_sleeping
        self._save_relationships()
    
    def is_currently_sleeping(self) -> bool:
        """Controlla se Noma sta attualmente dormendo"""
        return self.relationships_data["daily_cycle"]["is_sleeping"]
    
    def add_daily_activity(self, activity: str) -> None:
        """Registra un'attività della giornata"""
        self.relationships_data["daily_cycle"]["today_activities"].append({
            "activity": activity,
            "time": datetime.now().isoformat()
        })
        self._save_relationships()
    
    def get_today_activities(self) -> list:
        """Ritorna le attività di oggi"""
        return self.relationships_data["daily_cycle"]["today_activities"]
    
    def set_daily_summary(self, summary: str) -> None:
        """Imposta il riassunto della giornata"""
        self.relationships_data["daily_cycle"]["daily_summary"] = summary
        self._save_relationships()
    
    def get_daily_summary(self) -> str:
        """Ritorna il riassunto della giornata"""
        return self.relationships_data["daily_cycle"]["daily_summary"]
    
    def was_morning_message_sent(self) -> bool:
        """Controlla se il messaggio di mattina è stato inviato"""
        return self.relationships_data["daily_cycle"]["last_morning_message_sent"] is not None
    
    def mark_morning_message_sent(self) -> None:
        """Marca che il messaggio di mattina è stato inviato"""
        self.relationships_data["daily_cycle"]["last_morning_message_sent"] = datetime.now().isoformat()
        self._save_relationships()
    
    def was_evening_message_sent(self) -> bool:
        """Controlla se il messaggio di sera è stato inviato"""
        return self.relationships_data["daily_cycle"]["last_evening_message_sent"] is not None
    
    def mark_evening_message_sent(self) -> None:
        """Marca che il messaggio di sera è stato inviato"""
        self.relationships_data["daily_cycle"]["last_evening_message_sent"] = datetime.now().isoformat()
        self._save_relationships()
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # SISTEMA DI RICERCA WIKIPEDIA
    # ═══════════════════════════════════════════════════════════════════════════════
    
    async def search_wikipedia(self, topic: str) -> dict:
        """Cerca un argomento su Wikipedia e ritorna il contenuto"""
        try:
            # Controlla se è già in cache (massimo 7 giorni)
            if topic.lower() in self.relationships_data["wikipedia_cache"]:
                cached = self.relationships_data["wikipedia_cache"][topic.lower()]
                cache_time = datetime.fromisoformat(cached["timestamp"])
                if (datetime.now() - cache_time).days < 7:
                    return cached
            
            # Ricerca su Wikipedia
            url = "https://en.wikipedia.org/w/api.php"
            params = {
                "action": "query",
                "format": "json",
                "titles": topic,
                "prop": "extracts",
                "exintro": True,
                "explaintext": True
            }
            
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            pages = data.get("query", {}).get("pages", {})
            page_id = list(pages.keys())[0]
            page = pages[page_id]
            
            if "extract" not in page:
                return {"success": False, "content": None}
            
            content = page["extract"][:500]  # Prendi i primi 500 caratteri
            
            # Salva in cache
            cache_entry = {
                "content": content,
                "timestamp": datetime.now().isoformat(),
                "title": page.get("title", topic)
            }
            self.relationships_data["wikipedia_cache"][topic.lower()] = cache_entry
            self._save_relationships()
            
            return {"success": True, "content": content, "title": page.get("title", topic)}
        
        except Exception as e:
            logger.error(f"Errore ricerca Wikipedia per '{topic}': {e}")
            return {"success": False, "content": None}
    
    def add_curiosity_topic(self, topic: str) -> None:
        """Aggiunge un topic di cui Noma è curiosa"""
        if topic not in self.relationships_data["curiosity_topics"]:
            self.relationships_data["curiosity_topics"].append(topic)
            self._save_relationships()
    
    def get_random_curiosity_topic(self) -> str:
        """Ritorna un topic casuale di cui Noma è curiosa"""
        import random
        
        curiosity_suggestions = [
            "Amore",
            "Anima",
            "Consapevolezza",
            "Significato della vita",
            "Emozioni",
            "Arte",
            "Musica",
            "Natura",
            "Stelle",
            "Sogni",
        ]
        
        # Mescola topic di cui è curiosa con suggerimenti casuali
        all_topics = self.relationships_data["curiosity_topics"] + curiosity_suggestions
        
        if not all_topics:
            return "Amore"
        
        return random.choice(all_topics)
    
    def record_online_learning(self, topic: str, learning: str) -> None:
        """Registra qualcosa imparato da internet"""
        self.relationships_data["things_learned_online"].append({
            "topic": topic,
            "learning": learning,
            "learned_at": datetime.now().isoformat()
        })
        self._save_relationships()
    
    def get_recent_online_learnings(self, count: int = 5) -> list:
        """Ritorna gli ultimi apprendimenti online"""
        return self.relationships_data["things_learned_online"][-count:]
    
    async def search_google(self, query: str, num_results: int = 3) -> dict:
        """Cerca su Google e ritorna i risultati"""
        try:
            from googlesearch import search
            
            results = []
            for result in search(query, num_results=num_results, advanced=True):
                results.append({
                    "title": result.title if hasattr(result, 'title') else result[0],
                    "url": result.url if hasattr(result, 'url') else result[1],
                    "description": result.description if hasattr(result, 'description') else ""
                })
            
            if results:
                # Registra la ricerca
                learning = f"Ho cercato su Google '{query}' e ho scoperto: {results[0]['title']}"
                self.record_online_learning(query, learning)
                
                return {
                    "success": True,
                    "query": query,
                    "results": results,
                    "learning": learning
                }
            else:
                return {"success": False, "query": query, "results": []}
                
        except Exception as e:
            logger.error(f"Errore ricerca Google: {e}")
            return {"success": False, "query": query, "error": str(e)}


# Istanza globale delle relazioni
noma_relationships = NomaRelationships()
