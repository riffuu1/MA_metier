import tkinter as tk
from ui.login import LoginScreen
from ui.inscription import RegisterScreen
from ui.interface import MetierScreen
from ui.forum import ForumScreen
from ui.admin_panel import AdminScreen

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CPNV")
        self.state("zoomed")
        self.configure(bg="#FAF3E0")
        self.current_screen = None
        self.current_user = None  # stocke l'utilisateur connecté
        self.show_login()

    def clear_screen(self):
        if self.current_screen:
            self.current_screen.destroy()

    # -------------------------
    # LOGIN
    # -------------------------
    def show_login(self):
        self.clear_screen()
        self.current_screen = LoginScreen(
            self,
            self.show_register,
            self.show_interface
        )

    # -------------------------
    # REGISTER
    # -------------------------
    def show_register(self):
        self.clear_screen()
        self.current_screen = RegisterScreen(
            self,
            self.show_login
        )

    # -------------------------
    # METIER / DOMAINES
    # -------------------------
    def show_interface(self, user):
        self.current_user = user
        self.clear_screen()
        self.current_screen = MetierScreen(
            self,
            self.show_forum,
            user=user
        )

    def show_metier(self, domain):
        self.clear_screen()
        self.current_screen = MetierScreen(
            self,
            self.show_forum,
            user=self.current_user
        )
        self.current_screen.open_domain(domain)

    # -------------------------
    # FORUM
    # -------------------------
    def show_forum(self, domain):
        self.clear_screen()

        self.current_screen = ForumScreen(
            self,
            domain=domain,  # dictionnaire complet du domaine
            retour_callback=lambda d=domain: self.show_metier(d),  # retourne au sous-domaine
            user=self.current_user
        )
        self.current_screen.pack(fill="both", expand=True)

    #---------------------------
    # ADMIN PANEL
    #---------------------------
    def show_admin_screen(self):
        self.clear_screen()
        self.current_screen = AdminScreen(
            self,
            user=self.current_user,
            retour_callback=lambda: self.show_interface(self.current_user)
        )


if __name__ == "__main__":
    app = App()
    app.mainloop()
