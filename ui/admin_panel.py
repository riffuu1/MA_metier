import tkinter as tk
from tkinter import messagebox, simpledialog
import requests

API_ADMIN = "http://127.0.0.1:5000/admin/users"

class AdminScreen(tk.Frame):
    def __init__(self, master, user, retour_callback):
        super().__init__(master, bg="#FAF3E0")
        self.master = master
        self.user = user
        self.retour_callback = retour_callback

        self.pack(fill="both", expand=True)

        tk.Label(
            self,
            text="🛠️ Administration",
            font=("Helvetica", 20, "bold"),
            bg="#FAF3E0"
        ).pack(pady=10)

        # Bouton retour
        tk.Button(
            self,
            text="← Retour",
            font=("Helvetica", 12, "bold"),
            command=self.retour_callback
        ).pack(pady=10)

        self.list_frame = tk.Frame(self, bg="#FAF3E0")
        self.list_frame.pack(fill="both", expand=True, padx=20)

        self.charger_utilisateurs()


    def charger_utilisateurs(self):
        """Récupère la liste depuis Flask."""
        for w in self.list_frame.winfo_children():
            w.destroy()

        try:
            resp = requests.get(API_ADMIN, headers={"X-User-Role": "admin"})
            resp.raise_for_status()
            users = resp.json()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger les utilisateurs\n{e}")
            return

        for u in users:
            frame = tk.Frame(self.list_frame, bg="white", bd=1, relief="solid")
            frame.pack(fill="x", pady=5)

            tk.Label(frame, text=f"{u['firstname']} {u['lastname']} ({u['email']}) - {u['role']}", bg="white").pack(side="left", padx=10)

            tk.Button(frame, text="✏️", command=lambda u=u: self.edit_user(u)).pack(side="right", padx=5)
            tk.Button(frame, text="🗑️", fg="red", command=lambda u=u: self.delete_user(u)).pack(side="right", padx=5)

    def edit_user(self, user_data):
        popup = tk.Toplevel(self)
        popup.title("Modifier utilisateur")
        popup.geometry("420x320")
        popup.configure(bg="#FAF3E0")
        popup.transient(self)
        popup.grab_set()

        tk.Label(popup, text="Modifier utilisateur", font=("Helvetica", 16, "bold"),
                 bg="#FAF3E0").pack(pady=10)

        # -------- FORM --------
        form = tk.Frame(popup, bg="#FAF3E0")
        form.pack(padx=20, pady=10, fill="x")

        def field(label, value):
            tk.Label(form, text=label, bg="#FAF3E0").pack(anchor="w")
            e = tk.Entry(form)
            e.insert(0, value or "")
            e.pack(fill="x", pady=5)
            return e

        firstname_entry = field("Prénom", user_data["firstname"])
        lastname_entry = field("Nom", user_data["lastname"])
        email_entry = field("Email", user_data["email"])

        tk.Label(form, text="Rôle", bg="#FAF3E0").pack(anchor="w")
        role_var = tk.StringVar(value=user_data["role"])
        role_menu = tk.OptionMenu(form, role_var, "user", "admin")
        role_menu.pack(fill="x", pady=5)

        # -------- ACTIONS --------
        def submit():
            payload = {
                "data": {
                    "firstname": firstname_entry.get().strip(),
                    "lastname": lastname_entry.get().strip(),
                    "email": email_entry.get().strip(),
                    "role": role_var.get()
                }
            }

            if not all(payload["data"].values()):
                messagebox.showerror("Erreur", "Tous les champs sont requis")
                return

            try:
                resp = requests.put(
                    f"{API_ADMIN}/{user_data['id']}",
                    json=payload,
                    headers={"X-User-Role": "admin"}
                )
                resp.raise_for_status()
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de modifier\n{e}")
                return

            popup.destroy()
            self.charger_utilisateurs()

        btns = tk.Frame(popup, bg="#FAF3E0")
        btns.pack(pady=15)

        tk.Button(btns, text="Annuler", command=popup.destroy).pack(side="left", padx=10)
        tk.Button(btns, text="Valider", font=("Helvetica", 12, "bold"),
                  bg="#6D6875", fg="white", command=submit).pack(side="right", padx=10)

    def delete_user(self, user_data):
        if not messagebox.askyesno("Supprimer", f"Supprimer {user_data['firstname']} {user_data['lastname']} ?"):
            return

        try:
            resp = requests.delete(f"{API_ADMIN}/{user_data['id']}", headers={"X-User-Role": "admin"})
            resp.raise_for_status()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de supprimer\n{e}")
            return

        self.charger_utilisateurs()

    def go_back(self):
        self.destroy()
        self.master.show_interface(self.user)
