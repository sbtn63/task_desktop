import tkinter as tk
import customtkinter as ctk

class CustomDialog(ctk.CTkToplevel):
    def __init__(self, parent, title, message):
        super().__init__(parent)

        self.title(title)
        self.geometry("300x150")
        self.resizable(False, False)

        self.label = ctk.CTkLabel(self, text=message, wraplength=250, font=("Helvetica", 12))
        self.label.pack(pady=20, padx=20)

        self.ok_button = ctk.CTkButton(self, text="OK", command=self.destroy)
        self.ok_button.pack(pady=10)

    @staticmethod
    def show_error(parent, title, message):
        dialog = CustomDialog(parent, title, message)
        parent.wait_window(dialog)
