import os
import threading
import tkinter as tk
import tkinter.simpledialog as sd
import requests
from domain.entities import Enemy

class GUIAdapter:
    def __init__(self, service):
        self.service = service
        self.player = None
        self.chapter1_started = False
        self.chapter1_completed = False
        self.move_count = {'forward':0, 'right':0, 'left':0, 'back':0}
        self.current_npc_role = None

        self.root = tk.Tk()
        self.root.title("Crônicas Adaptativas")

        # Frame de início
        frm = tk.Frame(self.root)
        tk.Label(frm, text="Herói:").pack(side=tk.LEFT)
        self.ent = tk.Entry(frm)
        self.ent.pack(side=tk.LEFT)
        tk.Button(frm, text="Iniciar", command=self.init_game).pack(side=tk.LEFT)
        frm.pack(pady=5)

        # Log
        self.log = tk.Text(self.root, height=15, width=60, state=tk.DISABLED)
        self.log.pack(pady=5)

        # Status
        sfrm = tk.Frame(self.root)
        self.hp_label = tk.Label(sfrm, text="HP: --")
        self.hp_label.pack(side=tk.LEFT, padx=5)
        self.effects_label = tk.Label(sfrm, text="Efeitos: Nenhum")
        self.effects_label.pack(side=tk.LEFT, padx=5)
        sfrm.pack(pady=5)

        # Movimento
        mfrm = tk.Frame(self.root)
        tk.Button(mfrm, text="↑", width=3, command=self.move_forward).grid(row=0, column=1)
        tk.Button(mfrm, text="←", width=3, command=self.move_left).grid(row=1, column=0)
        tk.Button(mfrm, text="↓", width=3, command=self.move_back).grid(row=1, column=1)
        tk.Button(mfrm, text="→", width=3, command=self.move_right).grid(row=1, column=2)
        mfrm.pack(pady=5)

        # Conversa
        cfrm = tk.Frame(self.root)
        self.conv_entry = tk.Entry(cfrm, width=40)
        self.conv_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(cfrm, text="Conversar", command=self.send_conversation).pack(side=tk.LEFT)
        cfrm.pack(pady=5)

        # Ações
        afrm = tk.Frame(self.root)
        tk.Button(afrm, text="Quests", command=self.show_quests).pack(side=tk.LEFT, padx=3)
        tk.Button(afrm, text="Inventário", command=self.open_inventory).pack(side=tk.LEFT, padx=3)
        tk.Button(afrm, text="Sair", command=self.root.quit).pack(side=tk.LEFT, padx=3)
        afrm.pack(pady=5)

    def log_msg(self, msg: str):
        self.log.config(state=tk.NORMAL)
        self.log.insert(tk.END, msg + "\n\n")
        self.log.see(tk.END)
        self.log.config(state=tk.DISABLED)

    def init_game(self):
        name = self.ent.get().strip()
        if not name:
            return
        self.player = self.service.start_game(name)
        self.log_msg(f"Bem-vindo, {self.player.name}! Lv {self.player.level}")
        intro = (
            f"{self.player.name}, você desperta na pacata vila de Eldoria. "
            "Há rumores de monstros nas florestas próximas e perigos antigos adormecidos. "
            "Esta é sua primeira jornada: aventure-se além dos muros da aldeia e descubra seu destino! "
            "Verifique os objetivos da missão clicando no botão Quests."
        )
        self.log_msg("---")
        self.log_msg(intro)
        self.log_msg("---")

    def show_quests(self):
        if not self.player:
            return
        if not self.chapter1_started:
            self.log_msg("Objetivo da missão: Proteja ou fuja da vila.")
            self.chapter1_started = True
            self.root.after(3000, self.chapter1_attack)
        else:
            self.log_msg("Objetivo da missão: Proteja ou fuja da vila.")

    def chapter1_attack(self):
        self.log_msg("Um ataque surpresa começa! Você vê:")
        self.log_msg(" - Uma casa à sua frente")
        self.log_msg(" - Outra casa à direita")
        self.log_msg(" - Uma casa mais distante à esquerda")
        self.log_msg(" - A saída da vila atrás de você")

    def move_forward(self):
        self.log_msg("Você anda para frente.")
        self.move_count['forward'] += 1
        if self.chapter1_started and not self.chapter1_completed:
            self.log_msg("Você chega ao chalé do curandeiro. Ele oferece poções e cura ferimentos.")
            self.log_msg("O curandeiro pergunta:\n\"Você está ferido?\"")
            self.log_msg("Você pode responder com 'sim' ou 'não'.")
            self.log_msg("Se você responder 'sim', ele cura você e oferece poções.")
            self.log_msg("Se você responder 'não', ele oferece poções.")
            self.log_msg("Você pode usar poções para curar HP ou aumentar atributos.")
            self.log_msg("Você pode usar o campo 'Conversar' para falar com o curandeiro")
            self.current_npc_role = "curandeiro"
            self.log_msg(
                "Você entra no chalé do curandeiro. Aqui você pode: \n"
                " - **venda** de poções e remédios\n"
                " - **curar** de ferimentos\n"
                " - **treinar em magia** de cura\n"
                " - **conversar** sobre Eldoria"
            )
            self.chapter1_completed = True
            
    def move_right(self):
        self.log_msg("Você anda para a direita.")
        self.move_count['right'] += 1
        if self.chapter1_started and not self.chapter1_completed:
            self.log_msg("Você encontra a casa do antigo guerreiro. Ele pode treinar você em combate básico.")
            self.log_msg("O guerreiro pergunta:\n\"Você quer aprender a lutar?\"")
            self.log_msg("Você pode responder com 'sim' ou 'não'.")
            self.log_msg("Você pode usar o campo 'Conversar' para falar com o guerreiro")
            self.log_msg("Se você responder 'sim', ele ensina a lutar.")
            self.log_msg("Se você responder 'não', ele oferece dicas sobre o mundo.")
            self.log_msg(
                "Você entra na casa do guerreiro. Aqui você pode: \n"
                " - **treinar em combate\n"
                " - **treinar em magia** de combate\n"
                " - **conversar** sobre Eldoria"
            )

            self.current_npc_role = "guerreiro"
            self.chapter1_completed = True

    def move_left(self):
        self.log_msg("Você anda para a esquerda.")
        self.move_count['left'] += 1
        if self.chapter1_started and self.move_count['left'] >= 2 and not self.chapter1_completed:
            self.log_msg("Você encontra a casa do caçador, " \
            "o melhor arqueiro da região. Ele ensina técnicas de tiro.")
            self.log_msg("O caçador pergunta:\n\"Você quer aprender a atirar?\"")
            self.log_msg("Você pode responder com 'sim' ou 'não'.")
            self.log_msg("Você pode usar o campo 'Conversar' para falar com o caçador")
            self.log_msg("Se você responder 'sim', ele ensina a atirar.")
            self.log_msg("Se você responder 'não', ele oferece dicas sobre o mundo.")
            self.log_msg("Você pode usar o campo 'Conversar' para falar com o caçador")
            self.log_msg(
                "Você entra na casa do caçador. Aqui você pode: \n"
                " - **treinar em tiro**\n"
                " - **treinar em magia** de tiro\n"
                " - **conversar** sobre Eldoria"
            )
            self.log_msg("Você encontra o caçador. Palavra-chave: **conversar**.")
            self.current_npc_role = "caçador"
            self.chapter1_completed = True

    def move_back(self):
        self.log_msg("Você sai correndo pelos portões e deixa a vila para trás. Fim de jogo.")
        self.root.quit()

    def send_conversation(self):
        text = self.conv_entry.get().strip()
        if not text or not self.current_npc_role:
            self.log_msg("Nada a dizer no momento.")
            return
        self.log_msg(f"Você: {text}")
        self.conv_entry.delete(0, tk.END)
        self.ask_npc(text)

        if self.current_npc_role == "curandeiro":
            self.handle_curandeiro(text)
        else:
            self.ask_npc(text)
        if self.current_npc_role == "guerreiro":
            if 'treinar em combate' in text:
                self.service.train_combat(self.player)
                self.log_msg("**Guerreiro**: Você praticou **combate**. +1 Força.")
            elif 'treinar em magia' in text:
                self.service.train_magic(self.player)
                self.log_msg("**Guerreiro**: Você praticou **magia** de combate. +1 Inteligência.")
            elif 'conversar' in text:
                self.ask_npc(text)
            else:
                self.log_msg("**Guerreiro**: Use **treinar em combate**, **treinar em magia** ou **conversar**.")
        elif self.current_npc_role == "caçador":
            if 'treinar em tiro' in text:
                self.service.train_archery(self.player)
                self.log_msg("**Caçador**: Você praticou **tiro**. +1 Destreza.")
            elif 'treinar em magia' in text:
                self.service.train_magic(self.player)
                self.log_msg("**Caçador**: Você praticou **magia** de tiro. +1 Inteligência.")
            elif 'conversar' in text:
                self.ask_npc(text)
            else:
                self.log_msg("**Caçador**: Use **treinar em tiro**, **treinar em magia** ou **conversar**.")
    
    def handle_curandeiro(self, text: str):
        if 'venda' in text:
            self.log_msg("**Curandeiro**: Tenho Poção de Cura (50 ouro) e Elixir das Ervas (150 ouro).")
        elif 'curar' in text:
            self.service.heal_character(self.player)
            self.log_msg("**Curandeiro** lançou **Cura**. Seu HP foi totalmente restaurado.")
        elif 'treinar em magia' in text:
            self.service.train_magic(self.player)
            self.log_msg("**Curandeiro**: Você praticou **magia** de cura. +1 Inteligência.")
        elif 'conversar' in text:
            self.ask_npc(text)
        else:
            self.log_msg("**Curandeiro**: Use **venda**, **curar**, **treinar em magia** ou **conversar**.")

    def ask_npc(self, player_msg: str):
        def worker():
            #headers = {"Authorization": f"Bearer {API_KEY}"}
            system_prompt = f"Você é um {self.current_npc_role} sábio de Eldoria. Responda de forma imersiva."  
            data = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": player_msg}
                ]
            }
            resp = requests.post(
                #"https://api.openai.com/v1/chat/completions",
                json=data,
                headers=headers
            )
            if resp.status_code == 200:
                reply = resp.json()["choices"][0]["message"]["content"]
            else:
                reply = " Algo mais?"
                #reply = "... (não consegui me conectar ao oráculo)."
            self.root.after(0, lambda: self.log_msg(f"{self.current_npc_role.title()}: {reply}"))
        threading.Thread(target=worker, daemon=True).start()

    def open_inventory(self):
        inv = self.service.list_inventory(self.player)
        win = tk.Toplevel(self.root)
        win.title("Inventário")
        for item, qty in inv:
            frm = tk.Frame(win)
            tk.Label(frm, text=f"{item.name} x{qty}").pack(side=tk.LEFT)
            tk.Button(frm, text="Equipar", command=lambda i=item: self.equip_item(i)).pack(side=tk.LEFT, padx=2)
            tk.Button(frm, text="Usar", command=lambda i=item: self.use_item(i)).pack(side=tk.LEFT, padx=2)
            frm.pack(anchor="w", pady=2)

    def equip_item(self, item):
        self.log_msg(f"Você equipou: {item.name}")

    def use_item(self, item):
        self.log_msg(f"Você usou: {item.name}")

    def run(self):
        self.root.mainloop()