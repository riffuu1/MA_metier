import tkinter as tk
from tkinter import ttk, Toplevel
from PIL import Image, ImageTk

# ================== COULEURS ==================
BG_COLOR = "#FAF3E0"
TEXT_COLOR = "#6D6875"

# ================== FENÊTRE MÉTIER ==================
def ouvrir_metier(titre, description, points, image_path=None):
    fenetre = Toplevel()
    fenetre.title(titre)
    fenetre.configure(bg=BG_COLOR)
    fenetre.state("zoomed")
    fenetre.bind("<Escape>", lambda e: fenetre.destroy())

    # Bouton retour
    ttk.Button(fenetre, text="← Retour", style="Metier.TButton", command=fenetre.destroy).place(x=20, y=20)

    # Titre
    tk.Label(fenetre, text=titre, font=("Segoe UI", 30, "bold"), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=(60, 20))

    # ================= CONTENEUR PRINCIPAL =================
    main_container = tk.Frame(fenetre, bg=BG_COLOR)
    main_container.pack(fill="both", expand=True, padx=60, pady=30)
    main_container.grid_columnconfigure(0, weight=1)
    main_container.grid_columnconfigure(1, weight=4)
    main_container.grid_rowconfigure(0, weight=1)

    # ================= MENU GAUCHE =================
    menu_gauche = tk.Frame(main_container, bg=BG_COLOR, width=280)
    menu_gauche.grid(row=0, column=0, sticky="ns", padx=(0, 20))
    menu_gauche.grid_propagate(False)

    tk.Label(menu_gauche, text="Que veux-tu apprendre ?", font=("Segoe UI", 16, "bold"),
             bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=20)

    for item in ["Présentation", "Compétences", "Débouchés", "Formation"]:
        ttk.Button(menu_gauche, text=item, style="Metier.TButton").pack(fill="x", padx=20, pady=10)

    # ================= ZONE CONTENU DROITE =================
    contenu = tk.Frame(main_container, bg=BG_COLOR)
    contenu.grid(row=0, column=1, sticky="nsew")
    contenu.grid_columnconfigure(0, weight=1)

    # Image
    if image_path:
        try:
            img_pil = Image.open(image_path)
            img_pil = img_pil.resize((400, 300))
            img = ImageTk.PhotoImage(img_pil)
            label_img = tk.Label(contenu, image=img, bg=BG_COLOR)
            label_img.image = img
            label_img.pack(pady=20)
        except Exception as e:
            print("Erreur image :", e)

    # Texte
    texte_frame = tk.Frame(contenu, bg=BG_COLOR)
    texte_frame.pack(fill="both", expand=True, padx=40, pady=20)

    tk.Label(texte_frame, text=description, font=("Segoe UI", 15), bg=BG_COLOR, fg=TEXT_COLOR,
             wraplength=900, justify="left").pack(anchor="w", pady=(0, 20))

    for point in points:
        tk.Label(texte_frame, text="• " + point, font=("Segoe UI", 14), bg=BG_COLOR, fg=TEXT_COLOR,
                 justify="left").pack(anchor="w", pady=6)

# ================== FENÊTRE PRINCIPALE ==================
root = tk.Tk()
root.title("Découverte des métiers")
root.configure(bg=BG_COLOR)
root.state("zoomed")
root.bind("<Escape>", lambda e: root.destroy())

# Style des boutons
style = ttk.Style()
style.theme_use("clam")
style.configure("Metier.TButton", font=("Segoe UI", 11, "bold"), padding=10,
                foreground=TEXT_COLOR, background=BG_COLOR)

# Titres
tk.Label(root, text="Découverte des métiers", font=("Segoe UI", 28, "bold"),
         bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=25)
tk.Label(root, text="Clique sur un métier pour en savoir plus", font=("Segoe UI", 14),
         bg=BG_COLOR, fg=TEXT_COLOR).pack()

# Conteneur des cartes
frame_centrale = tk.Frame(root, bg=BG_COLOR)
frame_centrale.pack(pady=60)

# ================== CONTENUS MÉTIERS ==================
desc_info = "Dans la filière informatique du CPNV, le métier d’Informaticien·ne CFC consiste à concevoir, développer, installer et maintenir des systèmes informatiques."
points_info = ["Programmation et développement d’applications", "Gestion de bases de données", "Administration réseaux et sécurité", "Support et assistance utilisateurs"]

desc_media = "La médiamatique regroupe le multimédia, la communication, le marketing et l’informatique."
points_media = ["Création de contenus numériques", "Développement web et multimédia", "Communication digitale", "Gestion de projets créatifs"]

desc_poly = "La polymécanicien·ne fabrique des pièces mécaniques de haute précision."
points_poly = ["Usinage de pièces complexes", "Machines CNC", "Lecture de plans techniques", "Maintenance et prototypage"]

# ================== CARTES CLIQUABLES AVEC ANIMATION ==================
def creer_frame_metier(colonne, image, titre, desc, points, image_info):
    img_pil = Image.open(image)
    img_pil = img_pil.resize((350, 250))
    img = ImageTk.PhotoImage(img_pil)

    # Frame pour image + texte avec pady pour descendre les images
    cadre = tk.Frame(frame_centrale, bg=BG_COLOR)
    cadre.grid(row=0, column=colonne, padx=50, pady=50)  # <- images plus bas

    lbl_img = tk.Label(cadre, image=img, bg=BG_COLOR, cursor="hand2")
    lbl_img.image = img
    lbl_img.pack()

    lbl_titre = tk.Label(cadre, text=titre, font=("Segoe UI", 16, "bold"),
                         bg=BG_COLOR, fg=TEXT_COLOR)
    lbl_titre.pack(pady=10)

    # Animation "pulse" avant d'ouvrir la fenêtre métier
    def pulse_and_open():
        def grow(step=0):
            if step < 5:
                lbl_img.config(width=350 + step*5, height=250 + step*3)
                cadre.after(30, lambda: grow(step+1))
            else:
                shrink()

        def shrink(step=0):
            if step < 5:
                lbl_img.config(width=375 - step*5, height=265 - step*3)
                cadre.after(30, lambda: shrink(step+1))
            else:
                ouvrir_metier(titre, desc, points, image_info)

        grow()

    lbl_img.bind("<Button-1>", lambda e: pulse_and_open())
    lbl_titre.bind("<Button-1>", lambda e: pulse_and_open())

# Création des cartes
creer_frame_metier(0, "img.png", "Informatique", desc_info, points_info, "img_6.png")
creer_frame_metier(1, "img_1.png", "Médiamatique", desc_media, points_media, "img_4.png")
creer_frame_metier(2, "img_2.png", "Polymécanique", desc_poly, points_poly, "img_5.png")

root.mainloop()
