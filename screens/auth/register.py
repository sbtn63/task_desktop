import tkinter as tk
import customtkinter as ctk

from auth.user import register_user, validate_data
from components.custom_dialog import CustomDialog
from screens.tasks import home
from screens.auth import login

class RegisterFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(9, weight=1)

        self.label = ctk.CTkLabel(self, text="Register", font=("Helvetica", 16))
        self.label.grid(row=1, column=0, pady=10, padx=10, sticky="n")

        self.username_label = ctk.CTkLabel(self, text="Username")
        self.username_label.grid(row=2, column=0, pady=5, padx=5, sticky="n")
        self.username_entry = ctk.CTkEntry(self, width=200)
        self.username_entry.grid(row=3, column=0, pady=5, padx=5, sticky="n")

        self.password_label = ctk.CTkLabel(self, text="Password")
        self.password_label.grid(row=4, column=0, pady=5, padx=5, sticky="n")
        self.password_entry = ctk.CTkEntry(self, show="*", width=200)
        self.password_entry.grid(row=5, column=0, pady=5, padx=5, sticky="n")
        
        self.password_confirmation_label = ctk.CTkLabel(self, text="Password Confirm")
        self.password_confirmation_label.grid(row=6, column=0, pady=5, padx=5, sticky="n")
        self.password_confirmation_entry = ctk.CTkEntry(self, show="*", width=200)
        self.password_confirmation_entry.grid(row=7, column=0, pady=5, padx=5, sticky="n")

        self.register_button = ctk.CTkButton(self, text="Register", command=self.register)
        self.register_button.grid(row=8, column=0, pady=10, padx=10, columnspan=2)

        self.login_button = ctk.CTkButton(
            self, 
            text="You already have an account?", 
            command=lambda: controller.show_frame(login.LoginFrame),
            fg_color="transparent",
            text_color="gray", 
            hover_color="lightblue" 
        )
        self.login_button.grid(row=9, column=0, pady=10, padx=10, columnspan=2, sticky="n")

    def clean_entries(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.password_confirmation_entry.delete(0, tk.END)
    
    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        password_confirmation = self.password_confirmation_entry.get()
             
        if password != password_confirmation:
            self.clean_entries()
            return CustomDialog.show_info(self, "Register", "Passwords not match!!")
        
        try: 
            validate_data(username, password)
            token = register_user(username, password)
            
            if token:
                self.clean_entries()
                self.controller.show_frame(home.HomeFrame)
            else:
                self.clean_entries()
                CustomDialog.show_info(self, "Register", "Register Failed!!")
        except ValueError as e:
            self.clean_entries()
            CustomDialog.show_info(self, "Register", f"{str(e)}!!")