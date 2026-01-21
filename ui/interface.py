import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

BG_COLOR = "#FAF3E0"
TEXT_COLOR = "#6D6875"
NAV_COLOR = "#D3D3D3"  # Gris clair pour la nav-bar

# Chemin vers MA_metier/images
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(BASE_DIR, "images")


class MetierScreen(tk.Frame):
    def __init__(self, master, show_forum_callback):
        super().__init__(master, bg=BG_COLOR)
        self.master = master
        self.show_forum_callback = show_forum_callback
        self.pack(fill="both", expand=True)

        # =================== DONNÉES DES MÉTIERS ===================
        self.metiers = {
            "Informatique": {
                "img": "img_6.png",
                "desc": "Le métier d’Informaticien·ne CFC consiste à concevoir, développer, installer et maintenir des systèmes informatiques.",
                "points": [
                    "Programmation et développement d’applications",
                    "Gestion de bases de données",
                    "Administration réseaux et sécurité",
                    "Support et assistance utilisateurs"
                ],
                "sous_domaines": {
                    "Python": "Python est un langage polyvalent pour développement et automatisation.",
                    "Gestion de bases de données": "Apprentissage des bases relationnelles, SQL et gestion des données."
                }
            },
            "Médiamatique": {
                "img": "img_4.png",
                "desc": "La médiamatique regroupe multimédia, communication, marketing et informatique.",
                "points": [
                    "Création de contenus numériques",
                    "Développement web et multimédia",
                    "Communication digitale",
                    "Gestion de projets créatifs"
                ],
                "sous_domaines": {
                    "Communication digitale": "Stratégies de communication sur différents médias.",
                    "Web & multimédia": "Création de sites web et contenus multimédias."
                }
            },
            "Polymécanique": {
                "img": "img_5.png",
                "desc": "Le/la polymécanicien·ne fabrique des pièces mécaniques de haute précision.",
                "points": [
                    "Usinage de pièces complexes",
                    "Machines CNC",
                    "Lecture de plans techniques",
                    "Maintenance et prototypage"
                ],
                "sous_domaines": {
                    "Usinage CNC": "Apprentissage de l’usinage sur machines à commandes numériques.",
                    "Prototypage": "Création et test de prototypes mécaniques."
                }
            }
        }

        self.show_main_view()

    # =================== ÉCRAN PRINCIPAL ===================
    def show_main_view(self):
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text="Découverte des métiers", font=("Segoe UI", 28, "bold"),
                 bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=20)
        tk.Label(self, text="Clique sur un métier pour en savoir plus", font=("Segoe UI", 14),
                 bg=BG_COLOR, fg=TEXT_COLOR).pack()

        frame_carte = tk.Frame(self, bg=BG_COLOR)
        frame_carte.pack(pady=40)

        for i, (titre, data) in enumerate(self.metiers.items()):
            self.creer_carte(frame_carte, i, titre, data)

    # =================== CARTES MÉTIERS ===================
    def creer_carte(self, parent, colonne, titre, metier):
        img_path = os.path.join(IMG_DIR, metier["img"])
        if not os.path.exists(img_path):
            print(f"Image manquante : {img_path}")
            return

        # Redimension proportionnel
        max_width, max_height = 350, 200
        img_pil = Image.open(img_path)
        w, h = img_pil.size
        ratio = min(max_width / w, max_height / h)
        img_pil = img_pil.resize((int(w * ratio), int(h * ratio)))

        img = ImageTk.PhotoImage(img_pil)

        cadre = tk.Frame(parent, bg=BG_COLOR)
        cadre.grid(row=0, column=colonne, padx=50, pady=50)

        lbl_img = tk.Label(cadre, image=img, bg=BG_COLOR, cursor="hand2")
        lbl_img.image = img
        lbl_img.pack(pady=5)

        lbl_titre = tk.Label(cadre, text=titre, font=("Segoe UI", 16, "bold"),
                             bg=BG_COLOR, fg=TEXT_COLOR)
        lbl_titre.pack(pady=5)

        lbl_img.bind("<Button-1>", lambda e, t=titre: self.show_metier_view(t))
        lbl_titre.bind("<Button-1>", lambda e, t=titre: self.show_metier_view(t))

    # =================== ÉCRAN MÉTIER ===================
    def show_metier_view(self, titre):
        for widget in self.winfo_children():
            widget.destroy()

        self.current_metier = self.metiers[titre]

        main_container = tk.Frame(self, bg=BG_COLOR)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # ===== NAV-BAR GAUCHE =====
        # ===== NAV-BAR GAUCHE =====
        nav_frame = tk.Frame(main_container, bg=NAV_COLOR, width=220)
        nav_frame.pack(side="left", fill="y")
        nav_frame.pack_propagate(False)

        tk.Label(nav_frame, text=titre, font=("Segoe UI", 16, "bold"), bg=NAV_COLOR, fg=TEXT_COLOR).pack(pady=15)

        # Bouton Intro pour revenir à la vue générale du métier
        ttk.Button(nav_frame, text="Intro", command=lambda: self.show_sous_domaine(None)).pack(fill="x", padx=10, pady=8)

        # Sous-domaines
        for sd, desc in self.current_metier["sous_domaines"].items():
            ttk.Button(nav_frame, text=sd, command=lambda s=sd: self.show_sous_domaine(s)).pack(fill="x", padx=10, pady=8)

        # Boutons Forum
        ttk.Button(nav_frame, text="→ Forum", command=lambda t=titre: self.show_forum_callback(t)).pack(fill="x", padx=10, pady=20)

        # Boutons Ajouter une nouvelle connaissance
        ttk.Button(nav_frame, text=" + Ajouter", command=lambda t=titre: self.show_forum_callback(t)).pack(fill="x", padx=10, pady=20)

        # Boutons Retour
        ttk.Button(nav_frame, text="← Retour", command=self.show_main_view).pack(fill="x", padx=10, pady=5)

        # ===== ZONE DROITE =====
        self.contenu_frame = tk.Frame(main_container, bg=BG_COLOR)
        self.contenu_frame.pack(side="right", fill="both", expand=True)

        # Affichage initial du métier
        self.show_sous_domaine(None)

    # =================== AFFICHAGE SOUS-DOMAINE OU MÉTIER ===================
    def show_sous_domaine(self, sous_domaine):
        for widget in self.contenu_frame.winfo_children():
            widget.destroy()

        if sous_domaine is None:
            desc = self.current_metier["desc"]
            points = self.current_metier["points"]
        else:
            desc = self.current_metier["sous_domaines"][sous_domaine]
            points = []

        # Image proportionnelle centrée
        img_path = os.path.join(IMG_DIR, self.current_metier["img"])
        if os.path.exists(img_path):
            max_width, max_height = 400, 180  # limite hauteur
            img_pil = Image.open(img_path)
            w, h = img_pil.size
            ratio = min(max_width / w, max_height / h)
            img_pil = img_pil.resize((int(w * ratio), int(h * ratio)))
            img = ImageTk.PhotoImage(img_pil)

            lbl_img = tk.Label(self.contenu_frame, image=img, bg=BG_COLOR)
            lbl_img.image = img
            lbl_img.pack(pady=10)
            lbl_img.pack_configure(anchor="center")

        # Description
        tk.Label(
            self.contenu_frame,
            text=desc,
            font=("Segoe UI", 14),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            wraplength=700,
            justify="left"
        ).pack(anchor="nw", pady=10, padx=20)  # <-- padding à gauche augmenté à 20

        # Points clés
        for p in points:
            tk.Label(
                self.contenu_frame,
                text="• " + p,
                font=("Segoe UI", 13),
                bg=BG_COLOR,
                fg=TEXT_COLOR,
                justify="left"
            ).pack(anchor="nw", pady=3, padx=40)  # <-- padding plus large pour décaler les bullets
