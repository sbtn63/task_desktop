import tkinter as tk
import customtkinter as ctk

from auth.user import logout_user
from auth.session import session
from components.custom_dialog import CustomDialog
from screens.auth import login

class HomeFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.label = ctk.CTkLabel(self, text="Home")
        self.label.pack(pady=10, padx=10)
        
        self.logout_button = ctk.CTkButton(self, text="Logout", command=self.logout)
        self.logout_button.pack()
    
    def logout(self):
        session.load_session()
        token = session.token
        
        if token:
            logout_user(token)
            self.controller.show_frame(login.LoginFrame)
        else:
            CustomDialog.show_error(self, "Logout", "Error Logout!!")     

