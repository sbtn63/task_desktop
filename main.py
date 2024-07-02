import tkinter as tk
import customtkinter as ctk
from tkinter import ttk

from db.config import initialize_db
from auth.session import session
from screens.auth import login, register
from screens.tasks import home

class LoadingFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.label = ctk.CTkLabel(self, text="Cargando...", font=("Helvetica", 16))
        self.label.pack(pady=20)
        self.spinner = ttk.Progressbar(self, mode='indeterminate')
        self.spinner.pack(pady=20)
        self.spinner.start()

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Gestor de Tareas")
        self.geometry("500x500")
        
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        self.frame_classes = (
            LoadingFrame,
            login.LoginFrame,
            register.RegisterFrame,
            home.HomeFrame,
        )
        
        self.loading_frame = LoadingFrame(parent=self.container, controller=self)
        self.loading_frame.grid(row=0, column=0, sticky="nsew")
        self.loading_frame.tkraise()

        self.after(100, self.check_session)

    def create_frames(self):
        for FrameClass in self.frame_classes:
            page_name = FrameClass.__name__
            frame = FrameClass(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, page_class):
        frame = self.frames[page_class.__name__]
        if hasattr(frame, 'refresh_user_info'):
            frame.refresh_user_info()
        if hasattr(frame, 'create_task_cards'):
            frame.create_task_cards()
        frame.tkraise()
    
    def check_session(self):
        session.load_session()
        self.create_frames()

        if session.token:
            self.show_frame(home.HomeFrame)
        else:
            self.show_frame(login.LoginFrame)

        self.loading_frame.destroy()
        
if __name__ == "__main__":
    initialize_db()
    app = App()
    app.mainloop()