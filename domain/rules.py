from domain.entities import Character, Enemy, Item
import random

class StatusEffect:
    def __init__(self, duration: int):
        self.duration = duration
    def apply(self, target):
        pass

class Poison(StatusEffect):
    def apply(self, target):
        damage = 2
        target.hp -= damage

class Stun(StatusEffect):
    def apply(self, target):
        target.stunned = True

class Buff(StatusEffect):
    def __init__(self, attr: str, amount:int, duration:int):
        super().__init__(duration)
        self.attr, self.amount = attr, amount
    def apply(self, target):
        setattr(target, self.attr, getattr(target, self.attr) + self.amount)

class CombatRule:
    @staticmethod
    def fight(char: Character, enemy: Enemy) -> tuple[bool, int]:
        # aplicar efeitos no personagem
        for effect in list(char.effects):
            effect.apply(char)
            effect.duration -= 1
            if effect.duration <= 0:
                char.effects.remove(effect)
        # calcular dano
        dmg = char.attributes['forca'] + random.randint(0, char.level)
        enemy.hp -= dmg
        victory = enemy.hp <= 0
        xp_gain = enemy.level * 20 if victory else 0
        return victory, xp_gain

class LootRule:
    @staticmethod
    def drop(enemy: Enemy):
        from domain.entities import Item
        return Item(id=f"it_{enemy.id}", name="Restos de Monstro", type="misc", value=enemy.level * 5)

class Economics:
    @staticmethod
    def sell_price(item: Item, reputation: int) -> int:
        base = item.value
        modifier = 1 + reputation * 0.01
        return int(base * modifier)