import tkinter as tk
from tkinter import messagebox
import requests

BG_COLOR = "#FAF3E0"
TEXT_COLOR = "#6D6875"
API_FORUM = "http://127.0.0.1:5000/forum/posts"


class ForumScreen(tk.Frame):
    def __init__(self, master, domain, retour_callback, user):
        super().__init__(master, bg=BG_COLOR)
        self.domain = domain
        self.retour_callback = retour_callback
        self.user = user

        self.pack(fill="both", expand=True)

        # ---------- TITRE ----------
        tk.Label(
            self,
            text=f"Forum - {domain['name']}",
            font=("Segoe UI", 24, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=10)

        # ---------- ZONE BLANCHE ----------
        white_frame = tk.Frame(self, bg="white", bd=1, relief="solid")
        white_frame.pack(fill="both", expand=True, padx=40, pady=10)

        # Canvas + Scrollbar pour posts
        self.canvas = tk.Canvas(white_frame, bg="white", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(white_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="white")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # ---------- ZONE SAISIE ----------
        entry_frame = tk.Frame(self, bg=BG_COLOR)
        entry_frame.pack(fill="x", padx=40, pady=(0, 10))

        self.entry_msg = tk.Entry(entry_frame, font=("Segoe UI", 12))
        self.entry_msg.pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 10))

        tk.Button(
            entry_frame,
            text="Envoyer",
            font=("Segoe UI", 11, "bold"),
            bg="#6D6875",
            fg="white",
            relief="flat",
            command=self.envoyer_message
        ).pack(side="right")

        # ---------- RETOUR ----------
        tk.Button(
            self,
            text="← Retour",
            font=("Segoe UI", 11, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            relief="flat",
            command=self.retour_callback
        ).pack(pady=(0, 15))

        self.charger_messages()

    # ---------- CHARGER ----------
    def charger_messages(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        try:
            resp = requests.get(API_FORUM, params={"domain_id": self.domain["id"]})
            resp.raise_for_status()
            posts = resp.json()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
            posts = []

        # On met les messages du plus ancien au plus récent
        for post in reversed(posts):
            frame = tk.Frame(self.scrollable_frame, bg="white", bd=1, relief="solid", padx=5, pady=5)
            frame.pack(fill="x", pady=5, padx=5)

            header = tk.Label(frame, text=f"{post['author']} ({post['created_at']})", font=("Segoe UI", 10, "bold"), bg="white", fg=TEXT_COLOR)
            header.pack(anchor="w")

            content = tk.Label(frame, text=post["content"], font=("Segoe UI", 11), bg="white", wraplength=700, justify="left")
            content.pack(anchor="w", pady=(2, 0))

            if self.user["role"] == "admin":
                tk.Button(frame, text="Supprimer", bg="red", fg="white", font=("Segoe UI", 9, "bold"),
                          command=lambda pid=post["id"]: self.supprimer_post(pid)).pack(anchor="e", pady=(2,0))

        # Scroll automatique vers le bas
        self.after(100, lambda: self.canvas.yview_moveto(1.0))

    # ---------- ENVOYER ----------
    def envoyer_message(self):
        msg = self.entry_msg.get().strip()
        if not msg:
            return

        payload = {
            "domain_id": self.domain["id"],
            "title": "Discussion",
            "content": msg,
            "author_id": self.user["id"]
        }

        try:
            requests.post(API_FORUM, json=payload).raise_for_status()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
            return

        self.entry_msg.delete(0, "end")
        self.charger_messages()

    # ---------- SUPPRIMER POST ----------
    def supprimer_post(self, post_id):
        if not messagebox.askyesno("Supprimer", "Voulez-vous vraiment supprimer ce post ?"):
            return
        try:
            requests.delete(f"{API_FORUM}/{post_id}", json={"user": self.user}).raise_for_status()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
            return
        self.charger_messages()
