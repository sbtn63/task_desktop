import tkinter as tk
from tkinter import ttk

from db.config import initialize_db
from auth.session import session
from screens.auth import login, register
from screens.tasks import home

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Gestor de Tareas")

        self.geometry("800x600")
        
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        self.frame_classes = (
            login.LoginFrame,
            register.RegisterFrame,
            home.HomeFrame,
            
        )
        
        for FrameClass in self.frame_classes:
            page_name = FrameClass.__name__
            frame = FrameClass(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        session.load_session()
        
        if session.token:
            self.show_frame(home.HomeFrame)
        else:
            self.show_frame(login.LoginFrame)

    def show_frame(self, page_class):
        frame = self.frames[page_class.__name__]
        frame.tkraise()

if __name__ == "__main__":
    initialize_db()
    app = App()
    app.mainloop()