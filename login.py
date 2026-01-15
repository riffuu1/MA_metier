
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

# ---------------- CENTRER FENETRE ----------------
def centrer_fenetre(fenetre, largeur, hauteur):
    ecran_largeur = fenetre.winfo_screenwidth()
    ecran_hauteur = fenetre.winfo_screenheight()
    x = (ecran_largeur // 2) - (largeur // 2)
    y = (ecran_hauteur // 2) - (hauteur // 2)
    fenetre.geometry(f"{largeur}x{hauteur}+{x}+{y}")

# ---------------- PAGE LOGIN ----------------
login = Tk()
login.title("Connexion - CPNV")
centrer_fenetre(login, 600, 600)  # Fenêtre plus grande
login.configure(bg=COULEUR_FOND)

frame_login = Frame(login, bg="white", bd=10, relief="flat")
frame_login.pack(expand=True, fill=BOTH, padx=50, pady=50)

# Titre
Label(frame_login, text="BIENVENUE AU CPNV", bg="white", fg=COULEUR_BOUTON,
      font=FONT_TITRE).pack(pady=(10, 8))
Label(frame_login, text="Connectez-vous pour accéder à votre espace",
      bg="white", fg="#888", font=("Helvetica", 12, "italic")).pack(pady=(0, 20))

# Image
img = Image.open("téléchargement (2).png")
img = img.resize((180, 140))
photo = ImageTk.PhotoImage(img)
Label(frame_login, image=photo, bg="white").pack(pady=15)

# Champs Email
Label(frame_login, text="Email", bg="white", fg=COULEUR_TEXTE,
      font=FONT_LABEL).pack(anchor="w", padx=10)
Entry(frame_login, font=FONT_LABEL, width=35, bd=2, relief="solid").pack(pady=(0, 18))

# Champs Mot de passe
Label(frame_login, text="Mot de passe", bg="white", fg=COULEUR_TEXTE,
      font=FONT_LABEL).pack(anchor="w", padx=10)
Entry(frame_login, font=FONT_LABEL, width=35, bd=2, relief="solid", show="•").pack(pady=(0, 25))

# Bouton
Button(frame_login, text="Se connecter", font=FONT_BOLD,
       bg=COULEUR_ACCENT, fg="white", activebackground=COULEUR_BOUTON,
       relief="flat", cursor="hand2", padx=25, pady=12).pack(pady=(0, 10))

login.mainloop()
