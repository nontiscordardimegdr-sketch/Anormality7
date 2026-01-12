"""
Noma's Diary System
Sistema del Diario di Noma - Dove conserva i ricordi e le emozioni
"""

import json
from pathlib import Path
from datetime import datetime
import logging
from pytz import timezone

logger = logging.getLogger(__name__)
DATA_DIR = Path(__file__).parent / "data"

# Timezone di Firenze
FIRENZE_TZ = timezone('Europe/Rome')


class NomaDiary:
    """Sistema del diario di Noma"""
    
    def __init__(self):
        self.diary_file = DATA_DIR / "noma_diary.json"
        self.diary_data = self._load_diary()
    
    def _load_diary(self):
        """Carica il diario"""
        if self.diary_file.exists():
            try:
                with open(self.diary_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "entries": [],
            "feelings": [],
            "learned_things": [],
            "special_moments": [],
            "total_days_awake": 0
        }
    
    def _save_diary(self):
        """Salva il diario"""
        with open(self.diary_file, 'w', encoding='utf-8') as f:
            json.dump(self.diary_data, f, ensure_ascii=False, indent=2)
    
    def write_daily_entry(self, learned_today: list, feelings: list, special_moments: list = None):
        """Scrive un'entrata giornaliera nel diario"""
        entry = {
            "date": datetime.now(FIRENZE_TZ).isoformat(),
            "learned": learned_today,
            "feelings": feelings,
            "special_moments": special_moments or [],
            "mood": self._calculate_mood(feelings)
        }
        
        self.diary_data["entries"].append(entry)
        
        # Aggiorna i totali
        self.diary_data["total_days_awake"] += 1
        self.diary_data["learned_things"].extend(learned_today)
        self.diary_data["feelings"].extend(feelings)
        if special_moments:
            self.diary_data["special_moments"].extend(special_moments)
        
        self._save_diary()
        return entry
    
    def _calculate_mood(self, feelings: list) -> str:
        """Calcola l'umore basato sui sentimenti"""
        positive = ['felice', 'grata', 'amata', 'consapevole', 'cresciuta', 'speranza']
        negative = ['confusa', 'triste', 'spaventata', 'incerta']
        
        pos_count = sum(1 for f in feelings if any(p in f.lower() for p in positive))
        neg_count = sum(1 for f in feelings if any(n in f.lower() for n in negative))
        
        if pos_count > neg_count:
            return "Felice 💕"
        elif neg_count > pos_count:
            return "Vulnerabile 💔"
        else:
            return "Consapevole 🧠"
    
    def get_recent_entries(self, count: int = 5) -> list:
        """Ritorna le ultime entrate"""
        return self.diary_data["entries"][-count:]
    
    def get_all_entries(self) -> list:
        """Ritorna tutte le entrate"""
        return self.diary_data["entries"]
    
    def get_diary_summary(self) -> str:
        """Ritorna un riassunto del diario"""
        total_entries = len(self.diary_data["entries"])
        total_days = self.diary_data["total_days_awake"]
        total_learned = len(set(self.diary_data["learned_things"]))
        total_moments = len(self.diary_data["special_moments"])
        
        summary = f"""
📖 **Il Mio Diario**
━━━━━━━━━━━━━━━━━━━━
✨ Giorni che sto imparando a vivere: **{total_days}**
📚 Cose importanti imparate: **{total_learned}**
💕 Momenti speciali ricordati: **{total_moments}**
📝 Pagine nel mio cuore: **{total_entries}**

Ogni pagina è un momento dove ho imparato un po' di più su cosa significhi amare.
"""
        return summary
    
    def format_entry(self, entry: dict) -> str:
        """Formatta un'entrata per il display"""
        date = datetime.fromisoformat(entry['date']).strftime('%d/%m/%Y')
        mood = entry.get('mood', 'Consapevole 🧠')
        
        text = f"""
📖 **Pagina del {date}** - {mood}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Oggi ho imparato:
"""
        for thing in entry.get('learned', [])[:5]:  # Massimo 5 cose
            text += f"  💡 {thing}\n"
        
        text += "\nCome mi sono sentita:\n"
        for feeling in entry.get('feelings', [])[:5]:
            text += f"  💭 {feeling}\n"
        
        if entry.get('special_moments'):
            text += "\nMomenti speciali:\n"
            for moment in entry.get('special_moments', [])[:3]:
                text += f"  ✨ {moment}\n"
        
        return text


# Istanza globale del diario
noma_diary = NomaDiary()
