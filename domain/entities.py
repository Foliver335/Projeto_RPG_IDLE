from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class Character:
    id: str
    name: str
    level: int = 1
    exp: int = 0
    attributes: Dict[str, int] = field(default_factory=lambda: {'forca':10,'agilidade':10,'inteligencia':10})
    hp: int = 100
    effects: List = field(default_factory=list)
    inventory: List['Item'] = field(default_factory=list)
    profession: str = 'Novato'

@dataclass
class Item:
    id: str
    name: str
    type: str
    value: int

@dataclass
class Enemy:
    id: str
    name: str
    level: int
    hp: int

@dataclass
class Quest:
    id: str
    description: str
    difficulty: int
    rewards: Dict[str, int]