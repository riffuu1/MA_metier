import tkinter as tk
from tkinter import ttk

BG_COLOR = "#FAF3E0"
TEXT_COLOR = "#6D6875"
ACCENT_COLOR = "#4A4E69"
BOUTON_COLOR = "#6D6875"
FONT_TITLE = ("Helvetica", 16, "bold")
FONT_LABEL = ("Helvetica", 12)
FONT_BOLD = ("Helvetica", 12, "bold")


def popup_add_knowledge(parent, metier, callback=None):
    """
    Ouvre une popup pour ajouter une nouvelle connaissance à un métier ou sous-domaine.
    :param parent: frame ou Tk racine
    :param metier: dictionnaire du métier ou sous-domaine
    :param callback: fonction appelée après validation
    """
    popup = tk.Toplevel(parent)
    popup.title("Ajouter une connaissance")
    popup.configure(bg=BG_COLOR)
    popup.geometry("450x350")
    popup.transient(parent)
    popup.grab_set()

    # Cadre interne
    frame = tk.Frame(popup, bg="white", bd=10, relief="flat")
    frame.pack(expand=True, padx=30, pady=30)

    # Titre
    tk.Label(frame, text="Ajouter une connaissance", font=FONT_TITLE,
             bg="white", fg=ACCENT_COLOR).pack(pady=(10, 15))

    # Champ Titre
    tk.Label(frame, text="Titre", font=FONT_LABEL, bg="white", fg=TEXT_COLOR).pack(anchor="w", pady=(5, 3))
    entry_titre = tk.Entry(frame, font=FONT_LABEL, width=40, bd=2, relief="solid")
    entry_titre.pack(pady=(0, 15))

    # Champ Description
    tk.Label(frame, text="Description", font=FONT_LABEL, bg="white", fg=TEXT_COLOR).pack(anchor="w", pady=(5, 3))
    entry_desc = tk.Text(frame, font=FONT_LABEL, width=40, height=6, bd=2, relief="solid")
    entry_desc.pack(pady=(0, 15))

    # Label pour messages d'erreur ou succès
    label_message = tk.Label(frame, text="", fg="red", bg="white", font=("Helvetica", 11, "bold"))
    label_message.pack(pady=(5, 10))

    # Fonction validation
    def valider():
        titre = entry_titre.get().strip()
        desc = entry_desc.get("1.0", "end").strip()

        if not titre or not desc:
            label_message.config(text="Veuillez remplir le titre et la description.", fg="red")
            return

        # Ajouter la connaissance au métier
        if "connaissances" not in metier:
            metier["connaissances"] = []
        metier["connaissances"].append({"titre": titre, "desc": desc})

        label_message.config(text="Connaissance ajoutée avec succès !", fg="green")

        # Appeler callback si besoin
        if callback:
            callback(titre, desc)

        # Fermer popup après un court délai
        popup.after(1000, popup.destroy)

    # Bouton valider
    tk.Button(frame, text="Ajouter", font=FONT_BOLD, bg=ACCENT_COLOR, fg="white",
              activebackground=BOUTON_COLOR, relief="flat", cursor="hand2",
              padx=20, pady=8, command=valider).pack(pady=(5, 10))
