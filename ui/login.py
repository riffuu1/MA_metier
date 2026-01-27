from tkinter import Frame, Label, Entry, Button
from PIL import Image, ImageTk
import os
import requests

COULEUR_FOND   = "#FAF3E0"
COULEUR_ACCENT = "#4A4E69"
COULEUR_BOUTON = "#6D6875"
COULEUR_TEXTE  = "#4A4E69"
FONT_TITRE     = ("Helvetica", 22, "bold")
FONT_LABEL     = ("Helvetica", 13)
FONT_BOLD      = ("Helvetica", 13, "bold")

API_URL = "http://127.0.0.1:5000/auth/login"

class LoginScreen(Frame):
    def __init__(self, root, show_register, show_interface):
        super().__init__(root, bg=COULEUR_FOND)
        self.root = root
        self.show_register = show_register
        self.show_interface = show_interface
        self.pack(fill="both", expand=True)

        frame_login = Frame(self, bg="white", bd=10, relief="flat")
        frame_login.pack(expand=True, padx=50, pady=50)

        Label(frame_login, text="BIENVENUE AU CPNV",
              bg="white", fg=COULEUR_ACCENT, font=FONT_TITRE).pack(pady=(10, 5))

        Label(frame_login, text="Connectez-vous pour accéder à votre espace",
              bg="white", fg="#888", font=("Helvetica", 12, "italic")).pack(pady=(0, 20))

        image_path = os.path.join(os.path.dirname(__file__), "../images/téléchargement (2).png")
        img = Image.open(image_path).resize((180, 140))
        self.photo = ImageTk.PhotoImage(img)
        Label(frame_login, image=self.photo, bg="white").pack(pady=15)

        # Email
        Label(frame_login, text="Email", bg="white",
              fg=COULEUR_TEXTE, font=FONT_LABEL).pack(anchor="w", padx=60)
        self.entry_email = Entry(frame_login, font=FONT_LABEL, width=35, bd=2, relief="solid")
        self.entry_email.pack(anchor="w", padx=60, pady=(0, 15))

        # Mot de passe
        Label(frame_login, text="Mot de passe", bg="white",
              fg=COULEUR_TEXTE, font=FONT_LABEL).pack(anchor="w", padx=60)
        self.entry_password = Entry(frame_login, font=FONT_LABEL, width=35,
                                    bd=2, relief="solid", show="•")
        self.entry_password.pack(anchor="w", padx=60, pady=(0, 25))

        Button(frame_login, text="Se connecter", font=FONT_BOLD,
               bg=COULEUR_ACCENT, fg="white",
               activebackground=COULEUR_BOUTON,
               relief="flat", cursor="hand2",
               padx=25, pady=12,
               command=self.login).pack()

        self.label_erreur = Label(frame_login, text="", fg="red",
                                  bg="white", font=("Helvetica", 11, "bold"))
        self.label_erreur.pack(pady=(10, 5))

        Button(frame_login, text="Pas encore de compte ? S'inscrire",
               font=("Helvetica", 11, "underline"),
               fg=COULEUR_ACCENT, bg="white",
               relief="flat", cursor="hand2",
               command=show_register).pack(pady=(15, 5))

    def login(self):
        email = self.entry_email.get().strip()
        password = self.entry_password.get().strip()

        if not email or not password:
            self.label_erreur.config(text="Veuillez remplir tous les champs")
            return

        try:
            response = requests.post(API_URL, json={
                "email": email,
                "password": password
            })

            data = response.json()

            if not data.get("success"):
                self.label_erreur.config(text=data.get("message", "Erreur inconnue"))
                return

            # 🔥 Création de l'utilisateur complet
            user = {
                "id": data.get("id"),
                "email": data.get("email"),
                "role": data.get("role")
            }

            # Passer l'utilisateur à l'interface
            self.show_interface(user=user)

        except Exception as e:
            self.label_erreur.config(text="Erreur de connexion au serveur")
            print(e)
