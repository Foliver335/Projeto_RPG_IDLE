
import sqlite3, json
from datetime import datetime
from domain.entities import Character, Item, Quest

class SQLiteAdapter:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self):
        c = self.conn.cursor()
        c.executescript('''
            CREATE TABLE IF NOT EXISTS character(id TEXT PRIMARY KEY, name TEXT, level INTEGER, exp INTEGER, profession TEXT);
            CREATE TABLE IF NOT EXISTS item(id TEXT PRIMARY KEY, name TEXT, type TEXT, value INTEGER);
            CREATE TABLE IF NOT EXISTS inventory(char_id TEXT, item_id TEXT, quantity INTEGER, PRIMARY KEY(char_id,item_id));
            CREATE TABLE IF NOT EXISTS quest(id TEXT PRIMARY KEY, description TEXT, difficulty INTEGER, rewards TEXT, char_id TEXT, active INTEGER);
            CREATE TABLE IF NOT EXISTS battle_history(id TEXT PRIMARY KEY, char_id TEXT, enemy_id TEXT, victory INTEGER, xp INTEGER, timestamp TEXT);
        ''')
        self.conn.commit()

    def next_id(self, table: str) -> str:
        cur = self.conn.cursor()
        cur.execute(f"SELECT COUNT(*) as cnt FROM {table}")
        cnt = cur.fetchone()['cnt']
        return f"{table[:3]}_{cnt+1}"

    def save_character(self, char: Character):
        self.conn.execute("INSERT OR REPLACE INTO character VALUES(?,?,?,?,?)", (char.id, char.name, char.level, char.exp, char.profession))
        self.conn.commit()

    def load_character(self, char_id: str) -> Character:
        row = self.conn.execute("SELECT * FROM character WHERE id=?", (char_id,)).fetchone()
        return Character(**row) if row else None

    def add_item(self, char_id: str, item: Item, qty:int=1):
        self.conn.execute("INSERT OR IGNORE INTO item VALUES(?,?,?,?)", (item.id, item.name, item.type, item.value))
        self.conn.execute("INSERT INTO inventory(char_id,item_id,quantity) VALUES(?,?,?) ON CONFLICT(char_id,item_id) DO UPDATE SET quantity=quantity+?", (char_id,item.id,qty,qty))
        self.conn.commit()

    def get_inventory(self, char_id: str):
        rows = self.conn.execute("SELECT i.*, inv.quantity FROM item i JOIN inventory inv ON i.id=inv.item_id WHERE inv.char_id=?", (char_id,)).fetchall()
        return [(Item(**dict(r)), r['quantity']) for r in rows]

    def save_quest(self, quest: Quest, char_id: str):
        self.conn.execute("INSERT OR REPLACE INTO quest VALUES(?,?,?,?,?,1)", (quest.id, quest.description, quest.difficulty, json.dumps(quest.rewards), char_id))
        self.conn.commit()

    def load_active_quests(self, char_id: str):
        rows = self.conn.execute("SELECT * FROM quest WHERE char_id=? AND active=1", (char_id,)).fetchall()
        quests = []
        for r in rows:
            d = dict(r)
            d['rewards'] = json.loads(d['rewards'])
            quests.append(Quest(**d))
        return quests

    def complete_quest(self, quest_id: str, char_id: str):
        self.conn.execute("UPDATE quest SET active=0 WHERE id=? AND char_id=?", (quest_id, char_id))
        self.conn.commit()

    def save_battle(self, char_id: str, enemy_id: str, victory: bool, xp: int):
        bid = self.next_id('battle_history')
        ts = datetime.now().isoformat()
        self.conn.execute("INSERT INTO battle_history VALUES(?,?,?,?,?,?)", (bid, char_id, enemy_id, int(victory), xp, ts))
        self.conn.commit()

    def load_battles_all(self):
        rows = self.conn.execute("SELECT * FROM battle_history").fetchall()
        return [dict(r) for r in rows]

    def load_all_quests(self):
        rows = self.conn.execute("SELECT * FROM quest").fetchall()
        qs = []
        for r in rows:
            d = dict(r); d['rewards'] = json.loads(d['rewards']); qs.append(d)
        return qs