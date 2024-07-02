import tkinter as tk
import customtkinter as ctk

from auth.user import authenticate_user, validate_data
from components.custom_dialog import CustomDialog
from screens.auth import register
from screens.tasks import home

class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(7, weight=1)

        self.label = ctk.CTkLabel(self, text="Login", font=("Helvetica", 16))
        self.label.grid(row=1, column=0, pady=10, padx=10, sticky="n")

        self.username_label = ctk.CTkLabel(self, text="Username")
        self.username_label.grid(row=2, column=0, pady=5, padx=5, sticky="n")
        self.username_entry = ctk.CTkEntry(self, width=200)
        self.username_entry.grid(row=3, column=0, pady=5, padx=5, sticky="n")

        self.password_label = ctk.CTkLabel(self, text="Password")
        self.password_label.grid(row=4, column=0, pady=5, padx=5, sticky="n")
        self.password_entry = ctk.CTkEntry(self, show="*", width=200)
        self.password_entry.grid(row=5, column=0, pady=5, padx=5, sticky="n")

        self.login_button = ctk.CTkButton(self, text="Login", command=self.login)
        self.login_button.grid(row=6, column=0, pady=10, padx=10, columnspan=2)

        self.register_button = ctk.CTkButton(
            self, 
            text="You do not have an account?", 
            command=lambda: controller.show_frame(register.RegisterFrame),
            fg_color="transparent",
            text_color="gray",
            hover_color="lightblue",
        )
        self.register_button.grid(row=7, column=0, pady=10, padx=10, columnspan=2, sticky="n")

    def clean_entries(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
    
    def validate_entries(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        try:
            validate_data(username, password)
            token = authenticate_user(username, password)
            if token:
                self.clean_entries()
                self.controller.show_frame(home.HomeFrame)
            else:
                self.clean_entries()
                CustomDialog.show_info(self, "Login", "Error Login!!")
        except ValueError as e:
            self.clean_entries()
            CustomDialog.show_info(self, "Login", f"{str(e)}!!")
        