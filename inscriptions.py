'''
name : inscriptions.py
author: Dylan
'''
from tkinter import *

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


def creer_compte():
    mdp = entry_mdp.get()
    confirm = entry_confirm.get()

    if mdp != confirm:
        label_erreur.config(text="Les mots de passe ne correspondent pas.")
        return

    label_erreur.config(text="Compte créé avec succès !", fg="green")

# ---------------- PAGE CREATION COMPTE ----------------
register = Tk()
register.title("Créer un compte - CPNV")
centrer_fenetre(register, 600, 600)
register.configure(bg=COULEUR_FOND)

frame_register = Frame(register, bg="white", bd=10, relief="flat")
frame_register.pack(expand=True, fill=BOTH, padx=50, pady=50)

# Titre
Label(frame_register, text="CRÉER UN COMPTE", bg="white", fg=COULEUR_ACCENT,
      font=FONT_TITRE).pack(pady=(10, 5))
Label(frame_register, text="Rejoignez la plateforme du CPNV",
      bg="white", fg="#888", font=("Helvetica", 12, "italic")).pack(pady=(0, 20))

# Champs Nom
Label(frame_register, text="Nom complet", bg="white", fg=COULEUR_TEXTE,
      font=FONT_LABEL).pack(anchor="w", padx=10)
Entry(frame_register, font=FONT_LABEL, width=35, bd=2, relief="solid").pack(pady=(0, 15))

# Champs Email
Label(frame_register, text="Email", bg="white", fg=COULEUR_TEXTE,
      font=FONT_LABEL).pack(anchor="w", padx=10)
Entry(frame_register, font=FONT_LABEL, width=35, bd=2, relief="solid").pack(pady=(0, 15))

# Champs Mot de passe
Label(frame_register, text="Mot de passe", bg="white", fg=COULEUR_TEXTE,
      font=FONT_LABEL).pack(anchor="w", padx=10)
entry_mdp = Entry(frame_register, font=FONT_LABEL, width=35, bd=2, relief="solid", show="•")
entry_mdp.pack(pady=(0, 15))

# Champs Confirmation
Label(frame_register, text="Confirmer le mot de passe", bg="white", fg=COULEUR_TEXTE,
      font=FONT_LABEL).pack(anchor="w", padx=10)
entry_confirm = Entry(frame_register, font=FONT_LABEL, width=35, bd=2, relief="solid", show="•")
entry_confirm.pack(pady=(0, 25))

# Bouton principal
Button(frame_register, text="Créer le compte", font=FONT_BOLD,
       bg=COULEUR_ACCENT, fg="white", activebackground=COULEUR_BOUTON,
       relief="flat", cursor="hand2", padx=25, pady=12,
       command=creer_compte).pack()

# Label d’erreur
label_erreur = Label(frame_register, text="", fg="red", bg="white",
                     font=("Helvetica", 11, "bold"))
label_erreur.pack(pady=(10, 5))

# Bouton Déjà un compte
Button(frame_register, text="Déjà un compte ? Se connecter",
       font=("Helvetica", 11, "underline"), fg=COULEUR_ACCENT,
       bg="white", relief="flat", cursor="hand2",
       activeforeground=COULEUR_BOUTON).pack(pady=(15, 5))

register.mainloop()