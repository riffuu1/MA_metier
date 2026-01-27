from tkinter import Frame, Label, Entry, Button
import requests

COULEUR_FOND   = "#FAF3E0"
COULEUR_ACCENT = "#4A4E69"
COULEUR_BOUTON = "#6D6875"
COULEUR_TEXTE  = "#4A4E69"
FONT_TITRE     = ("Helvetica", 22, "bold")
FONT_LABEL     = ("Helvetica", 13)
FONT_BOLD      = ("Helvetica", 13, "bold")

API_URL = "http://127.0.0.1:5000/auth/register"  # <-- important

class RegisterScreen(Frame):
    def __init__(self, root, show_login):
        super().__init__(root, bg=COULEUR_FOND)
        self.root = root
        self.show_login = show_login
        self.pack(fill="both", expand=True)

        frame_reg = Frame(self, bg="white", bd=10, relief="flat")
        frame_reg.pack(expand=True, padx=50, pady=50)

        Label(frame_reg, text="CRÉER UN COMPTE",
              bg="white", fg=COULEUR_ACCENT, font=FONT_TITRE).pack(pady=(10, 5))

        # Email
        Label(frame_reg, text="Email", bg="white",
              fg=COULEUR_TEXTE, font=FONT_LABEL).pack(anchor="w", padx=60)
        self.entry_email = Entry(frame_reg, font=FONT_LABEL, width=35, bd=2, relief="solid")
        self.entry_email.pack(anchor="w", padx=60, pady=(0, 15))

        # Prénom
        Label(frame_reg, text="Prénom", bg="white",
              fg=COULEUR_TEXTE, font=FONT_LABEL).pack(anchor="w", padx=60)
        self.entry_firstname = Entry(frame_reg, font=FONT_LABEL, width=35, bd=2, relief="solid")
        self.entry_firstname.pack(anchor="w", padx=60, pady=(0, 15))

        # Nom
        Label(frame_reg, text="Nom", bg="white",
              fg=COULEUR_TEXTE, font=FONT_LABEL).pack(anchor="w", padx=60)
        self.entry_lastname = Entry(frame_reg, font=FONT_LABEL, width=35, bd=2, relief="solid")
        self.entry_lastname.pack(anchor="w", padx=60, pady=(0, 15))

        # Mot de passe
        Label(frame_reg, text="Mot de passe", bg="white",
              fg=COULEUR_TEXTE, font=FONT_LABEL).pack(anchor="w", padx=60)
        self.entry_password = Entry(frame_reg, font=FONT_LABEL, width=35,
                                    bd=2, relief="solid", show="•")
        self.entry_password.pack(anchor="w", padx=60, pady=(0, 25))

        # Bouton inscription
        Button(frame_reg, text="S'inscrire", font=FONT_BOLD,
               bg=COULEUR_ACCENT, fg="white",
               activebackground=COULEUR_BOUTON,
               relief="flat", cursor="hand2",
               padx=25, pady=12,
               command=self.register).pack()

        self.label_erreur = Label(frame_reg, text="", fg="red",
                                  bg="white", font=("Helvetica", 11, "bold"))
        self.label_erreur.pack(pady=(10, 5))

        # Retour login
        Button(frame_reg, text="Déjà un compte ? Se connecter",
               font=("Helvetica", 11, "underline"),
               fg=COULEUR_ACCENT, bg="white",
               relief="flat", cursor="hand2",
               command=show_login).pack(pady=(15, 5))

    # =================== REGISTER FLASK ===================
    def register(self):
        email = self.entry_email.get().strip()
        firstname = self.entry_firstname.get().strip()
        lastname = self.entry_lastname.get().strip()
        password = self.entry_password.get().strip()

        if not email or not firstname or not lastname or not password:
            self.label_erreur.config(text="Veuillez remplir tous les champs")
            return

        try:
            response = requests.post(API_URL, json={
                "email": email,
                "firstname": firstname,
                "lastname": lastname,
                "password": password
            })

            data = response.json()

            if not data.get("success"):
                self.label_erreur.config(text=data.get("message", "Erreur inconnue"))
                return

            self.label_erreur.config(fg="green", text="Inscription réussie ! Vous pouvez vous connecter.")
            # Eventuellement rediriger vers l'écran login après 1-2s
            self.show_login()

        except Exception as e:
            self.label_erreur.config(text="Erreur de connexion au serveur")
            print(e)
