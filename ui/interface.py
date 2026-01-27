import tkinter as tk
from tkinter import messagebox
import requests

BG_COLOR = "#FAF3E0"
TEXT_COLOR = "#4A4E69"

API_DOMAINS = "http://127.0.0.1:5000/domains/"
API_KNOWLEDGE = "http://127.0.0.1:5000/knowledge/"


class MetierScreen(tk.Frame):
    def __init__(self, master, show_forum_callback, user):
        super().__init__(master, bg=BG_COLOR)
        self.master = master
        self.show_forum_callback = show_forum_callback
        self.user = user

        self.current_domain = None
        self.current_articles = []

        self.pack(fill="both", expand=True)
        self.show_domains_view()

    # -------------------------
    # PAGE DOMAINES PRINCIPALE
    # -------------------------
    def show_domains_view(self):
        self.clear()

        tk.Label(
            self,
            text="Choisissez un domaine",
            font=("Helvetica", 18, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=15)

        try:
            domains = requests.get(API_DOMAINS).json()
        except Exception as e:
            print("Erreur fetching domains:", e)
            domains = []

        for d in domains:
            frame = tk.Frame(self, bg="white", bd=2, relief="ridge", padx=10, pady=8)
            frame.pack(fill="x", padx=50, pady=5)

            name_btn_frame = tk.Frame(frame, bg="white")
            name_btn_frame.pack(fill="x")

            # Nom du domaine
            tk.Button(
                name_btn_frame,
                text=d["name"],
                font=("Helvetica", 14, "bold"),
                bg="white",
                fg=TEXT_COLOR,
                relief="flat",
                cursor="hand2",
                command=lambda dom=d: self.open_domain(dom)
            ).pack(side="left")

            if self.user["role"] == "admin":
                # Modifier domaine
                tk.Button(
                    name_btn_frame,
                    text="✏️",
                    font=("Helvetica", 11),
                    bg="white",
                    fg=TEXT_COLOR,
                    relief="flat",
                    cursor="hand2",
                    command=lambda dom=d: self.domain_popup(dom)
                ).pack(side="left", padx=5)

                # Supprimer domaine
                tk.Button(
                    name_btn_frame,
                    text="🗑️",
                    font=("Helvetica", 11),
                    bg="white",
                    fg="red",
                    relief="flat",
                    cursor="hand2",
                    command=lambda dom=d: self.delete_domain(dom)
                ).pack(side="left", padx=5)

        # Ajouter un domaine (admin)
        if self.user["role"] == "admin":
            tk.Button(
                self,
                text="➕ Ajouter un domaine",
                font=("Helvetica", 12, "bold"),
                bg=BG_COLOR,
                fg=TEXT_COLOR,
                relief="flat",
                cursor="hand2",
                command=self.domain_popup
            ).pack(pady=10)

        if self.user["role"] == "admin":
            tk.Button(self, text="💼 Admin", bg="#6D6875", fg="white",
                      font=("Segoe UI", 10, "bold"),
                      command=lambda: self.master.show_admin_screen()).place(relx=0.95, rely=0.02, anchor="ne")

    # -------------------------
    # OUVRIR UN DOMAINE / SOUS-DOMAINE
    # -------------------------
    def open_domain(self, domain):
        self.current_domain = domain
        self.clear()

        container = tk.Frame(self, bg=BG_COLOR)
        container.pack(fill="both", expand=True)

        nav = tk.Frame(container, bg="#EDE6D8", width=220)
        nav.pack(side="left", fill="y")

        content = tk.Frame(container, bg="white")
        content.pack(side="right", fill="both", expand=True)

        # Récupération articles / sous-domaines
        try:
            self.current_articles = requests.get(
                API_KNOWLEDGE,
                params={"domain_id": domain["id"]}
            ).json()
        except:
            self.current_articles = []

        # NAV BAR - titre
        tk.Label(nav, text=domain["name"], font=("Helvetica", 14, "bold"), bg="#EDE6D8").pack(pady=10)

        # BOUTON RETOUR → page domaines
        tk.Button(nav, text="← Retour", bg="#6D6875", fg="white",
                  font=("Helvetica", 12, "bold"), relief="flat",
                  command=self.show_domains_view).pack(fill="x", padx=10, pady=(0, 10))

        # BOUTON FORUM → forum du domaine
        tk.Button(
            nav,
            text="💬 Forum",
            bg="#6D6875",
            fg="white",
            font=("Helvetica", 12, "bold"),
            relief="flat",
            command=lambda d=domain: self.show_forum_callback(d)  # on envoie juste le domain
        ).pack(fill="x", padx=10, pady=(0, 15))

        # Bouton Introduction
        tk.Button(nav, text="📘 Introduction", command=lambda: self.show_intro(content)) \
            .pack(fill="x", padx=10, pady=5)

        # Boutons articles / sous-domaines
        for art in self.current_articles:
            tk.Button(nav, text=art["title"], command=lambda a=art: self.show_article(content, a)) \
                .pack(fill="x", padx=10, pady=2)

        # ➕ Ajouter un sous-domaine (TOUT LE MONDE)
        tk.Button(nav, text="➕ Ajouter un sous-domaine", command=self.article_popup) \
            .pack(fill="x", padx=10, pady=15)

        # Affiche introduction par défaut
        self.show_intro(content)

    # -------------------------
    # INTRODUCTION
    # -------------------------
    def show_intro(self, frame):
        self.clear_frame(frame)
        tk.Label(frame, text=self.current_domain["name"], font=("Helvetica", 16, "bold"), bg="white").pack(pady=10)
        tk.Label(frame, text=self.current_domain.get("description", "Aucune description"),
                 wraplength=700, justify="left", bg="white").pack(padx=20, pady=10)

    # -------------------------
    # AFFICHER ARTICLE
    # -------------------------
    def show_article(self, frame, article):
        self.clear_frame(frame)
        tk.Label(frame, text=article["title"], font=("Helvetica", 16, "bold"), bg="white").pack(pady=10)
        tk.Label(frame, text=article["content"], wraplength=700, justify="left", bg="white").pack(padx=20, pady=10)

        if self.user["role"] == "admin":
            tk.Button(frame, text="✏️ Modifier", command=lambda: self.article_popup(article)).pack(side="left", padx=20, pady=10)
            tk.Button(frame, text="🗑️ Supprimer", command=lambda: self.delete_article(article)).pack(side="left", padx=5, pady=10)

    # -------------------------
    # POP-UP ARTICLE / SOUS-DOMAINE
    # -------------------------
    def article_popup(self, article=None):
        popup = tk.Toplevel(self)
        popup.title("Sous-domaine")
        popup.geometry("420x320")
        popup.configure(bg=BG_COLOR)

        tk.Label(popup, text="Titre :", bg=BG_COLOR).pack(pady=5)
        title_entry = tk.Entry(popup, width=45)
        title_entry.pack()
        tk.Label(popup, text="Contenu :", bg=BG_COLOR).pack(pady=5)
        content_entry = tk.Text(popup, height=8, width=45)
        content_entry.pack()

        if article:
            title_entry.insert(0, article["title"])
            content_entry.insert("1.0", article["content"])

        def submit():
            title = title_entry.get().strip()
            content = content_entry.get("1.0", "end").strip()
            if not title or not content:
                tk.messagebox.showerror("Erreur", "Titre et contenu requis")
                return

            payload = {
                "user": self.user,
                "domain_id": self.current_domain["id"],
                "title": title,
                "content": content,
                "author_id": self.user["id"]
            }

            try:
                if article:
                    if self.user["role"] == "admin":
                        requests.put(f"{API_KNOWLEDGE}{article['id']}", json=payload)
                else:
                    response = requests.post(API_KNOWLEDGE, json=payload)
                    if response.status_code != 200:
                        tk.messagebox.showerror("Erreur", response.json().get("message", "Erreur ajout"))
                        return
            except Exception as e:
                tk.messagebox.showerror("Erreur", f"Impossible de sauvegarder\n{e}")
                return

            popup.destroy()
            self.open_domain(self.current_domain)

        tk.Button(popup, text="Valider", font=("Helvetica", 12, "bold"),
                  bg="#6D6875", fg="white", command=submit).pack(pady=15)

    # -------------------------
    # POP-UP DOMAINES (ADMIN)
    # -------------------------
    def domain_popup(self, domain=None):
        popup = tk.Toplevel(self)
        popup.title("Domaine")
        popup.geometry("400x200")
        popup.configure(bg=BG_COLOR)

        tk.Label(popup, text="Nom :", bg=BG_COLOR).pack(pady=5)
        name_entry = tk.Entry(popup, width=40)
        name_entry.pack(pady=5)
        tk.Label(popup, text="Description :", bg=BG_COLOR).pack(pady=5)
        desc_entry = tk.Entry(popup, width=40)
        desc_entry.pack(pady=5)

        if domain:
            name_entry.insert(0, domain["name"])
            desc_entry.insert(0, domain.get("description", ""))

        def submit():
            name = name_entry.get().strip()
            desc = desc_entry.get().strip()
            if not name:
                return

            payload = {"name": name, "description": desc, "user": self.user}

            if domain:
                requests.put(f"{API_DOMAINS}{domain['id']}", json=payload)
            else:
                requests.post(API_DOMAINS, data={"name": name, "role": self.user["role"], "description": desc})

            popup.destroy()
            self.show_domains_view()

        tk.Button(popup, text="Valider", command=submit).pack(pady=15)

    # -------------------------
    # SUPPRIMER DOMAINES / ARTICLES
    # -------------------------
    def delete_domain(self, domain):
        if not messagebox.askyesno("Supprimer", f"Supprimer {domain['name']} ?"):
            return
        requests.delete(f"{API_DOMAINS}{domain['id']}", json={"user": self.user})
        self.show_domains_view()

    def delete_article(self, article):
        if not messagebox.askyesno("Supprimer", f"Supprimer {article['title']} ?"):
            return
        requests.delete(f"{API_KNOWLEDGE}{article['id']}", json={"user": self.user})
        self.open_domain(self.current_domain)

    # -------------------------
    # UTILITAIRES
    # -------------------------
    def clear(self):
        for w in self.winfo_children():
            w.destroy()

    def clear_frame(self, frame):
        for w in frame.winfo_children():
            w.destroy()
