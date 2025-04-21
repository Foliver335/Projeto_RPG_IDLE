from pymongo import MongoClient
from domain.entities import Character, Item, Quest

class MongoAdapter:
    def __init__(self, uri:str="mongodb://localhost:27017"):
        client = MongoClient(uri)
        self.db = client['cronicas']
    def save_character(self, char: Character):
        self.db.characters.replace_one({'id':char.id}, char.__dict__, upsert=True)