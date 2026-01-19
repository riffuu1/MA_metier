import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

# ================== COULEURS ==================
BG_COLOR = "#FAF3E0"
TEXT_COLOR = "#6D6875"
MSG_USER_BG = "#D9E6F2"

# ================== BASE DE DONNÉES ==================
base_utilisateurs = ["Lucas", "Dylan", "Imad", "Eldan"]

# ================== VARIABLES ==================
utilisateur_actif = None
historique_messages = {}  # {user: [(msg, vu)]}

# ================== FENÊTRE ==================
root = tk.Tk()
root.title("ForumCpnv.core")
root.configure(bg=BG_COLOR)
root.state("zoomed")  # Plein écran

# ================== STYLE ==================
style = ttk.Style()
style.theme_use("default")
style.configure("Chat.TButton", font=("Segoe UI", 11, "bold"), padding=8)

# ================== CONTENEUR ==================
main = tk.Frame(root, bg=BG_COLOR)
main.pack(fill="both", expand=True)

# ================== MENU GAUCHE ==================
menu = tk.Frame(main, bg=BG_COLOR, width=260)
menu.pack(side="left", fill="y")
menu.pack_propagate(False)

tk.Label(menu, text="Contacts", font=("Segoe UI", 18, "bold"),
         bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=20)

frame_contacts = tk.Frame(menu, bg=BG_COLOR)
frame_contacts.pack(fill="both", expand=True)

# ================== ZONE CHAT ==================
chat = tk.Frame(main, bg=BG_COLOR)
chat.pack(side="right", fill="both", expand=True)

messages = scrolledtext.ScrolledText(chat, font=("Segoe UI", 12),
                                     bg=BG_COLOR, fg=TEXT_COLOR)
messages.pack(fill="both", expand=True, padx=20, pady=(20, 10))
messages.config(state="disabled")

# ================== BARRE MESSAGE ==================
entry_frame = tk.Frame(chat, bg=BG_COLOR)
entry_frame.pack(fill="x", padx=20, pady=(0, 20))

entry_msg = tk.Entry(entry_frame, font=("Segoe UI", 12), state="disabled")
entry_msg.pack(side="left", fill="x", expand=True, padx=(0, 10), ipady=6)

btn_envoyer = ttk.Button(entry_frame, text="Envoyer", state="disabled")
btn_envoyer.pack(side="right")

# ================== FONCTIONS ==================
def afficher_messages(user):
    messages.config(state="normal")
    messages.delete("1.0", "end")

    for msg, vu in historique_messages.get(user, []):
        status = "✔ Vu" if vu else "Envoyé"
        messages.insert("end", f"Moi : {msg}   ({status})\n")

    messages.config(state="disabled")
    messages.yview("end")

def selectionner_utilisateur(user):
    global utilisateur_actif
    utilisateur_actif = user

    # Marquer tous les messages comme vus
    historique_messages[user] = [(m, True) for m, _ in historique_messages.get(user, [])]

    entry_msg.config(state="normal")
    btn_envoyer.config(state="normal")

    afficher_messages(user)

def envoyer_message():
    msg = entry_msg.get().strip()
    if not msg or not utilisateur_actif:
        return

    historique_messages.setdefault(utilisateur_actif, [])
    historique_messages[utilisateur_actif].append((msg, False))

    entry_msg.delete(0, "end")
    afficher_messages(utilisateur_actif)

btn_envoyer.config(command=envoyer_message)

# ================== AJOUT UTILISATEUR ==================
def ajouter_utilisateur():
    popup = tk.Toplevel(root)
    popup.title("Ajouter utilisateur")
    popup.geometry("420x240")
    popup.configure(bg=BG_COLOR)
    popup.transient(root)
    popup.focus_force()

    # Centrer la popup
    popup.update_idletasks()
    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()
    win_width = popup.winfo_width()
    win_height = popup.winfo_height()
    x = (screen_width // 2) - (win_width // 2)
    y = (screen_height // 2) - (win_height // 2)
    popup.geometry(f"{win_width}x{win_height}+{x}+{y}")

    tk.Label(popup, text="Ajouter un utilisateur",
             font=("Segoe UI", 16, "bold"),
             bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=20)

    entry = tk.Entry(popup, font=("Segoe UI", 12))
    entry.pack(padx=40, fill="x")
    entry.focus()

    def valider():
        nom = entry.get().strip()
        if nom in base_utilisateurs:
            if nom not in historique_messages:
                historique_messages[nom] = []

            btn = ttk.Button(frame_contacts, text=nom,
                             command=lambda n=nom: selectionner_utilisateur(n),
                             style="Chat.TButton")
            btn.pack(fill="x", padx=20, pady=6)
            popup.destroy()
        else:
            messagebox.showerror("Erreur", "Utilisateur introuvable! ")

    ttk.Button(popup, text="Ajouter", command=valider).pack(pady=15)

    # ================== BOUTON SUPPORT ==================
    def contacter_support():
        messagebox.showinfo(
            "Support",
            "Contactez le support à l'adresse :\n\nsupport@cpnv.core-app.com"
        )

    btn_support = tk.Button(
        popup,
        text="Besoin d’aide ? Contacter le support",
        command=contacter_support,
        font=("Segoe UI", 10, "underline"),
        fg="#3A6EA5",
        bg=BG_COLOR,
        bd=0,
        activebackground=BG_COLOR,
        cursor="hand2"
    )
    btn_support.pack(pady=(5, 0))

# ================== BOUTON AJOUT ==================
ttk.Button(menu, text="+ Ajouter un utilisateur",
           command=ajouter_utilisateur,
           style="Chat.TButton").pack(padx=20, pady=15)

root.mainloop()
