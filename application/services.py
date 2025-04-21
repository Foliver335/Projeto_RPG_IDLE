from datetime import datetime
from domain.rules import CombatRule, LootRule
from domain.entities import Character, Enemy, Quest, Item
from adapters.db.sqlite_adapter import SQLiteAdapter
from adapters.ml.recommender import Recommender

class GameService:
    def __init__(self, db: SQLiteAdapter, ml: Recommender):
        self.db = db
        self.ml = ml

    def start_game(self, name: str) -> Character:
        cid = self.db.next_id('character')
        char = Character(id=cid, name=name)
        self.db.save_character(char)
        return char

    def idle_tick(self, char: Character) -> int:
        data = self.db.load_character(char.id)
        gained = 5 + data.level
        char.exp = data.exp + gained
        if char.exp >= char.level * 100:
            char.exp -= char.level * 100
            char.level += 1
        self.db.save_character(char)
        return gained

    def fight_enemy(self, char: Character, enemy: Enemy) -> str:
        win, xp = CombatRule.fight(char, enemy)
        self.db.save_battle(char.id, enemy.id, win, xp)
        if win:
            char.exp += xp
            loot = LootRule.drop(enemy)
            self.db.add_item(char.id, loot)
            self.db.save_character(char)
            return f"Venceu! +{xp} XP e loot: {loot.name}"
        return "Derrotado... tente outra vez."

    def list_inventory(self, char: Character):
        return self.db.get_inventory(char.id)

    def generate_quests(self, char: Character) -> list[Quest]:
        active = self.db.load_active_quests(char.id)
        if active:
            return active
        suggestions = self.ml.suggest_quests(self.db.load_character(char.id).__dict__)
        for q in suggestions:
            self.db.save_quest(q, char.id)
        return suggestions

    def complete_quest(self, char: Character, quest_id: str) -> str:
        active = self.db.load_active_quests(char.id)
        q = next((x for x in active if x.id == quest_id), None)
        if not q:
            return "Quest não encontrada ou já concluída"
        for it, val in q.rewards.items():
            item = Item(id=f"itm_{it}", name=it, type='misc', value=val)
            self.db.add_item(char.id, item, val)
        self.db.complete_quest(quest_id, char.id)
        return f"Quest {quest_id} concluída! Recompensas concedidas."