# adapters/ui/cli_adapter.py
import os
import threading
import time
import requests
from application.services import GameService

API_KEY = os.getenv('OPENAI_API_KEY')  # defina no ambiente

class CLIAdapter:
    def __init__(self, service: GameService):
        self.service = service
        self.player = None
        self.chapter1_started = False
        self.chapter1_completed = False
        self.move_count = {'forward':0, 'right':0, 'left':0, 'back':0}
        self.current_npc_role = None

    def run(self):
        name = input("Herói, digite seu nome: ").strip()
        if not name:
            return
        self.player = self.service.start_game(name)
        print(f"\nBem-vindo, {self.player.name}! Lv {self.player.level}\n")
        print(f"{self.player.name}, você desperta na pacata vila de Eldoria.")
        print("Verifique os objetivos da missão com 'quest'.\n")

        while True:
            cmd = input("Comando [quest/move <direção>/converse/inv/sair]: ").strip().lower()
            if cmd == 'quest':
                self.show_quests()
            elif cmd.startswith('move'):
                parts = cmd.split()
                if len(parts) == 2:
                    self.handle_move(parts[1])
                else:
                    print("Use: move forward/back/left/right")
            elif cmd == 'converse':
                self.send_conversation()
            elif cmd == 'inv':
                self.show_inventory()
            elif cmd == 'sair':
                print("Até a próxima aventura!")
                break
            else:
                print("Comando inválido.")

    def show_quests(self):
        if not self.chapter1_started:
            print("Objetivo da missão: Proteja ou fuja da vila.")
            self.chapter1_started = True
            threading.Timer(3, self.chapter1_attack).start()
        else:
            print("Objetivo da missão: Proteja ou fuja da vila.")

    def chapter1_attack(self):
        print("\nUm ataque surpresa começa! Você vê:")
        print(" - Uma casa à sua frente")
        print(" - Outra casa à direita")
        print(" - Uma casa mais distante à esquerda")
        print(" - A saída da vila atrás de você\n")

    def handle_move(self, direction: str):
        if not self.chapter1_started:
            print("Use 'quest' primeiro.")
            return
        dir_map = {'forward': 'frente', 'back': 'atrás', 'left': 'esquerda', 'right': 'direita'}
        if direction not in dir_map:
            print("Direção inválida.")
            return
        print(f"Você anda para {dir_map[direction]}.\n")
        self.move_count[direction] += 1
        if direction == 'back':
            print("Você deixa a vila para trás. Fim de jogo.")
            exit()
        if self.chapter1_completed:
            return
        if direction == 'forward':
            self.current_npc_role = 'curandeiro'
            print("Você chega ao chalé do curandeiro. Palavras-chave: **venda**, **curar**, **treinar em magia**, **conversar**.")
        elif direction == 'right':
            self.current_npc_role = 'guerreiro'
            print("Você encontra o guerreiro. Palavras-chave: **treinar em magia**, **conversar**.")
        elif direction == 'left' and self.move_count['left'] >= 2:
            self.current_npc_role = 'caçador'
            print("Você encontra o caçador. Palavra-chave: **conversar**.")
        else:
            return
        self.chapter1_completed = True

    def send_conversation(self):
        if not self.current_npc_role:
            print("Nada a dizer no momento.")
            return
        text = input("Você: ").strip().lower()
        if 'venda' in text and self.current_npc_role == 'curandeiro':
            print("Curandeiro: Tenho Poção de Cura (50 ouro) e Elixir das Ervas (150 ouro).")
        elif 'curar' in text and self.current_npc_role == 'curandeiro':
            self.service.heal_character(self.player)
            print("Curandeiro lançou Cura. HP restaurado.")
        elif 'treinar em magia' in text and self.current_npc_role in ['curandeiro','guerreiro']:
            self.service.train_magic(self.player)
            print(f"{self.current_npc_role.title()}: Treinamento concluído. +1 Inteligência.")
        elif 'conversar' in text:
            self.ask_npc(text)
        else:
            print("Use as palavras-chave indicadas.")

    def ask_npc(self, player_msg: str):
        headers = {"Authorization": f"Bearer {API_KEY}"}
        system_prompt = f"Você é um {self.current_npc_role} sábio de Eldoria."
        data = {"model":"gpt-3.5-turbo","messages":[{"role":"system","content":system_prompt},{"role":"user","content":player_msg}]}
        resp = requests.post("https://api.openai.com/v1/chat/completions", json=data, headers=headers)
        if resp.status_code == 200:
            reply = resp.json()["choices"][0]["message"]["content"]
        else:
            reply = "... erro de conexão."
        print(f"{self.current_npc_role.title()}: {reply}\n")

    def show_inventory(self):
        inv = self.service.list_inventory(self.player)
        print("\nInventário:")
        for item, qty in inv:
            print(f"- {item.name} x{qty}")
        print()  # espaço
        
        if not inv:
            print("Inventário vazio.")
        else:
            print("Use 'usar <item>' para usar um item.")
            print("Use 'descartar <item>' para descartar um item.")
            action = input("Ação: ").strip().lower()
            parts = action.split()
            if len(parts) == 2 and parts[0] in ['usar', 'descartar']:
                item_name = parts[1]
                if parts[0] == 'usar':
                    self.service.use_item(self.player, item_name)
                    print(f"Usou {item_name}.")
                elif parts[0] == 'descartar':
                    self.service.discard_item(self.player, item_name)
                    print(f"Descartou {item_name}.")