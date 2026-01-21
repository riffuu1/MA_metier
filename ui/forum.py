import tkinter as tk
from tkinter import ttk, scrolledtext
from ui.interface import MetierScreen  # si besoin

BG_COLOR = "#FAF3E0"
TEXT_COLOR = "#6D6875"

class ForumScreen(tk.Frame):
    def __init__(self, master, metier, retour_callback):
        super().__init__(master, bg=BG_COLOR)
        self.master = master
        self.metier = metier
        self.retour_callback = retour_callback
        self.pack(fill="both", expand=True)

        # Titre
        tk.Label(self, text=f"Forum - {metier}", font=("Segoe UI", 24, "bold"),
                 bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=20)

        # Zone messages
        self.messages = scrolledtext.ScrolledText(self, font=("Segoe UI", 12),
                                                  bg=BG_COLOR, fg=TEXT_COLOR, height=15)
        self.messages.pack(fill="both", expand=True, padx=20)
        self.messages.config(state="disabled")

        # Barre saisie
        entry_frame = tk.Frame(self, bg=BG_COLOR)
        entry_frame.pack(fill="x", padx=20, pady=10)

        self.entry_msg = tk.Entry(entry_frame, font=("Segoe UI", 12))
        self.entry_msg.pack(side="left", fill="x", expand=True, padx=(0,10), ipady=6)

        ttk.Button(entry_frame, text="Envoyer", command=self.envoyer_message).pack(side="right")

        # Bouton Retour
        ttk.Button(self, text="← Retour", command=self.retour_callback).pack(pady=10)

    def envoyer_message(self):
        msg = self.entry_msg.get().strip()
        if msg:
            self.messages.config(state="normal")
            self.messages.insert("end", f"Moi : {msg}\n")
            self.messages.config(state="disabled")
            self.messages.yview("end")
            self.entry_msg.delete(0, "end")
