'''
name : inscriptions.py
author: Dylan
'''
from tkinter import Frame, Label, Entry, Button

# ---------------- CONFIG DESIGN ----------------
COULEUR_FOND   = "#FAF3E0"
COULEUR_ACCENT = "#4A4E69"
COULEUR_BOUTON = "#6D6875"
COULEUR_TEXTE  = "#4A4E69"
FONT_TITRE     = ("Helvetica", 22, "bold")
FONT_LABEL     = ("Helvetica", 13)
FONT_BOLD      = ("Helvetica", 13, "bold")


class RegisterScreen(Frame):
    def __init__(self, root, show_login):
        super().__init__(root, bg=COULEUR_FOND)
        self.pack(fill="both", expand=True)

        frame_register = Frame(self, bg="white", bd=10, relief="flat")
        frame_register.pack(expand=True, padx=50, pady=50)

        # Titre
        Label(
            frame_register,
            text="CRÉER UN COMPTE",
            bg="white",
            fg=COULEUR_ACCENT,
            font=FONT_TITRE
        ).pack(pady=(10, 5))

        Label(
            frame_register,
            text="Rejoignez la plateforme du CPNV",
            bg="white",
            fg="#888",
            font=("Helvetica", 12, "italic")
        ).pack(pady=(0, 20))

        # Champs Nom
        Label(
            frame_register,
            text="Nom complet",
            bg="white",
            fg=COULEUR_TEXTE,
            font=FONT_LABEL
        ).pack(anchor="w", padx=60)

        self.entry_nom = Entry(
            frame_register,
            font=FONT_LABEL,
            width=35,
            bd=2,
            relief="solid"
        )
        self.entry_nom.pack(anchor="w", padx=60, pady=(0, 15))

        # Champs Email
        Label(
            frame_register,
            text="Email",
            bg="white",
            fg=COULEUR_TEXTE,
            font=FONT_LABEL
        ).pack(anchor="w", padx=60)

        self.entry_email = Entry(
            frame_register,
            font=FONT_LABEL,
            width=35,
            bd=2,
            relief="solid"
        )
        self.entry_email.pack(anchor="w", padx=60, pady=(0, 15))

        # Mot de passe
        Label(
            frame_register,
            text="Mot de passe",
            bg="white",
            fg=COULEUR_TEXTE,
            font=FONT_LABEL
        ).pack(anchor="w", padx=60)

        self.entry_mdp = Entry(
            frame_register,
            font=FONT_LABEL,
            width=35,
            bd=2,
            relief="solid",
            show="•"
        )
        self.entry_mdp.pack(anchor="w", padx=60, pady=(0, 15))

        # Confirmation
        Label(
            frame_register,
            text="Confirmer le mot de passe",
            bg="white",
            fg=COULEUR_TEXTE,
            font=FONT_LABEL
        ).pack(anchor="w", padx=60)

        self.entry_confirm = Entry(
            frame_register,
            font=FONT_LABEL,
            width=35,
            bd=2,
            relief="solid",
            show="•"
        )
        self.entry_confirm.pack(anchor="w", padx=60, pady=(0, 25))

        # Bouton créer compte
        Button(
            frame_register,
            text="Créer le compte",
            font=FONT_BOLD,
            bg=COULEUR_ACCENT,
            fg="white",
            activebackground=COULEUR_BOUTON,
            relief="flat",
            cursor="hand2",
            padx=25,
            pady=12,
            command=self.creer_compte
        ).pack()

        # Message erreur
        self.label_erreur = Label(
            frame_register,
            text="",
            fg="red",
            bg="white",
            font=("Helvetica", 11, "bold")
        )
        self.label_erreur.pack(pady=(10, 5))

        # Retour login
        Button(
            frame_register,
            text="Déjà un compte ? Se connecter",
            font=("Helvetica", 11, "underline"),
            fg=COULEUR_ACCENT,
            bg="white",
            relief="flat",
            cursor="hand2",
            activeforeground=COULEUR_BOUTON,
            command=show_login
        ).pack(pady=(15, 5))

    def creer_compte(self):
        nom = self.entry_nom.get()
        email = self.entry_email.get()
        mdp = self.entry_mdp.get()
        confirm = self.entry_confirm.get()

        if not nom or not email or not mdp or not confirm:
            self.label_erreur.config(
                text="Veuillez remplir tous les champs.",
                fg="red"
            )
            return

        if mdp != confirm:
            self.label_erreur.config(
                text="Les mots de passe ne correspondent pas.",
                fg="red"
            )
            return

        self.label_erreur.config(
            text="Compte créé avec succès !",
            fg="green"
        )
