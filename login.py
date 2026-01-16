'''
name : login.py
author: Dylan
'''
from tkinter import *
from PIL import Image, ImageTk

# ---------------- CONFIG DESIGN ----------------
COULEUR_FOND   = "#FAF3E0"
COULEUR_ACCENT = "#4A4E69"
COULEUR_BOUTON = "#6D6875"
COULEUR_TEXTE  = "#4A4E69"
FONT_TITRE     = ("Helvetica", 22, "bold")
FONT_LABEL     = ("Helvetica", 13)
FONT_BOLD      = ("Helvetica", 13, "bold")

# ---------------- PAGE LOGIN ----------------
login = Tk()
login.title("Connexion - CPNV")

# plein écran
login.state("zoomed")

login.configure(bg=COULEUR_FOND)

frame_login = Frame(login, bg="white", bd=10, relief="flat")
frame_login.pack(expand=True, padx=50, pady=50)

# Titre
Label(frame_login, text="BIENVENUE AU CPNV", bg="white", fg=COULEUR_ACCENT,
      font=FONT_TITRE).pack(pady=(10, 5))

Label(frame_login, text="Connectez-vous pour accéder à votre espace",
      bg="white", fg="#888", font=("Helvetica", 12, "italic")).pack(pady=(0, 20))

# Image
img = Image.open("téléchargement (2).png")
img = img.resize((180, 140))
photo = ImageTk.PhotoImage(img)
Label(frame_login, image=photo, bg="white").pack(pady=15)

# Champs Email
Label(frame_login, text="Email", bg="white", fg=COULEUR_TEXTE,
      font=FONT_LABEL).pack(anchor="w", padx=60)

Entry(frame_login, font=FONT_LABEL, width=35,
      bd=2, relief="solid").pack(anchor="w", padx=60, pady=(0, 15))

# Champs Mot de passe
Label(frame_login, text="Mot de passe", bg="white", fg=COULEUR_TEXTE,
      font=FONT_LABEL).pack(anchor="w", padx=60)

Entry(frame_login, font=FONT_LABEL, width=35,
      bd=2, relief="solid", show="•").pack(anchor="w", padx=60, pady=(0, 25))

# Bouton connexion
Button(frame_login, text="Se connecter", font=FONT_BOLD,
       bg=COULEUR_ACCENT, fg="white", activebackground=COULEUR_BOUTON,
       relief="flat", cursor="hand2", padx=25, pady=12).pack()

# Message erreur
label_erreur = Label(frame_login, text="", fg="red", bg="white",
                     font=("Helvetica", 11, "bold"))
label_erreur.pack(pady=(10, 5))

# Bouton créer un compte
Button(frame_login, text="Pas encore de compte ? S'inscrire",
       font=("Helvetica", 11, "underline"), fg=COULEUR_ACCENT,
       bg="white", relief="flat", cursor="hand2",
       activeforeground=COULEUR_BOUTON).pack(pady=(15, 5))

login.mainloop()
