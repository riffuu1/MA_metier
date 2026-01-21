import tkinter as tk

from ui.login import LoginScreen
from ui.inscription import RegisterScreen
from ui.interface import MetierScreen
from ui.forum import ForumScreen


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("CPNV")
        self.state("zoomed")
        self.configure(bg="#FAF3E0")

        self.current_screen = None

        self.show_login()

    def clear_screen(self):
        if self.current_screen:
            self.current_screen.destroy()

    def show_login(self):
        self.clear_screen()
        self.current_screen = LoginScreen(
            self,
            self.show_register,
            self.show_interface
        )

    def show_register(self):
        self.clear_screen()
        self.current_screen = RegisterScreen(
            self,
            self.show_login
        )

    def show_interface(self):
        self.clear_screen()
        self.current_screen = MetierScreen(self, self.show_forum)

    def show_metier(self, metier):
        """Pour revenir dans l'écran métier depuis le forum"""
        self.clear_screen()
        self.current_screen = MetierScreen(self, self.show_forum)
        # Affiche directement le métier sélectionné
        self.current_screen.show_metier_view(metier)

    def show_forum(self, metier):
        self.clear_screen()
        self.current_screen = ForumScreen(self, metier, retour_callback=lambda: self.show_metier(metier))


if __name__ == "__main__":
    app = App()
    app.mainloop()
