import tkinter as tk
import customtkinter as ctk
from datetime import datetime

from db.config import get_conn
from auth.user import logout_user, get_user
from auth.session import session
from components.custom_dialog import CustomDialog
from screens.auth import login

now = datetime.now()

class HomeFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        #menu
        self.menu_frame = ctk.CTkFrame(self, fg_color="gray", corner_radius=0)
        self.menu_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        
        self.label = ctk.CTkLabel(
            self.menu_frame, 
            font=("Helvetica", 20), 
            text_color="white"
        )
        self.label.grid(row=0, column=0, pady=0, padx=5, sticky="w")
        
        self.logout_button = ctk.CTkButton(
            self.menu_frame, 
            text="Logout", 
            command=self.logout,
            text_color="white", 
            fg_color="red", 
            hover_color="darkred"
        )
        self.logout_button.grid(row=0, column=1, pady=5, padx=5, sticky="e")

        self.menu_frame.grid_columnconfigure(0, weight=1)
        self.menu_frame.grid_columnconfigure(1, weight=0)
        
        self.refresh_user_info()
        
        #list tasks
        # create tabview
        self.tabview = ctk.CTkTabview(self, width=250)
        self.tabview.grid(row=2, column=0, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.tabview.add("List Tasks")
        self.tabview.add("Create Task")
        self.tabview.tab("List Tasks").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Create Task").grid_columnconfigure(0, weight=1)

        # Crear un marco para las tarjetas de tarea
        self.cards_frame = ctk.CTkScrollableFrame(self.tabview.tab('List Tasks'))
        self.cards_frame.pack(fill="both", expand=True)

        self.create_task_cards()
        
        #form create task
        self.title_label = ctk.CTkLabel(self.tabview.tab("Create Task"), text="Title")
        self.title_label.grid(row=2, column=0, pady=5, padx=5, sticky="n")
        self.title_entry = ctk.CTkEntry(self.tabview.tab("Create Task"), width=200)
        self.title_entry.grid(row=3, column=0, pady=5, padx=5, sticky="n")
        
        self.content_label = ctk.CTkLabel(self.tabview.tab("Create Task"), text="Content")
        self.content_label.grid(row=4, column=0, pady=5, padx=5, sticky="n")
        self.content_entry = ctk.CTkTextbox(self.tabview.tab("Create Task"))
        self.content_entry.grid(row=5, column=0, pady=5, padx=5, sticky="n")
        
        self.create_button = ctk.CTkButton(self.tabview.tab("Create Task"), text="Create", command=self.create_task)
        self.create_button.grid(row=6, column=0, pady=10, padx=10, columnspan=2)
        
    def clean_entries(self):
        self.title_entry.delete(0, tk.END)
        self.content_entry.delete(1.0, tk.END)
    
    def validate_data(self, title):
        if title == '':
            raise ValueError('Title not valid')
        else:
            pass
    
    def refresh_user_info(self):
        session.load_session()
        username = session.username if session.username else "Guest"
        self.label.configure(text=f"@{username}")
    
    def create_task_cards(self):
        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        for item in self.get_task_user():
            card_frame = ctk.CTkFrame(
                self.cards_frame, 
                bg_color="lightgray", 
                corner_radius=5, 
                border_width=1, 
                border_color="gray"
            )
            card_frame.pack(pady=10, padx=10, fill="both", expand=True)

            title_label = ctk.CTkLabel(
                card_frame, text=item[1], 
                font=("Helvetica", 14, "bold")
            )
            title_label.pack(pady=(5, 10))

            content_label = ctk.CTkLabel(
                card_frame, 
                text=item[2], 
                font=("Helvetica", 12), 
                wraplength=250
            )
            content_label.pack(pady=(5, 10))
            
            if item[3] == 1:
                message = 'Completed'
            else:
                message = 'Incompleted'
            
            completed_label = ctk.CTkLabel(card_frame, text=message, font=("Helvetica", 12), wraplength=250)
            completed_label.pack(pady=(5, 10))

            if item[3] == 0:
                button_completed = ctk.CTkButton(
                    card_frame, 
                    text="Completed", 
                    fg_color="green", 
                    hover_color="darkred",
                    command=lambda task_id=item[0]: self.update_task_completed(task_id)
                )
                button_completed.pack(pady=(0, 10))

            button_delete = ctk.CTkButton(
                card_frame, 
                text="Delete", 
                fg_color="red", 
                hover_color="darkred",
                command=lambda task_id=item[0]: self.delete_task(task_id)
            )
            button_delete.pack(pady=(0, 10))
    
    def update_task_list(self):
        self.create_task_cards()
    
    def create_task(self):
        title = self.title_entry.get()
        content = self.content_entry.get(1.0, tk.END)
        
        try:
            self.validate_data(title)
        except ValueError as e:
            self.clean_entries()
            return CustomDialog.show_info(self, "Task", f"{str(e)}!!")
        
        user = get_user(session.token)
        
        if user is None:
            return CustomDialog.show_info(self, "Task", "User not exists")
        
        message = self.insert_task(title=title, user_id=user[0], content=content)
        if not str(message):
            self.clean_entries()
            CustomDialog.show_info(self, "Task", "Error created task!!")
            
        self.clean_entries()
        CustomDialog.show_info(self, "Task", message)
        self.update_task_list()
    
    def insert_task(self, title, user_id, content = None):
        with get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO tasks (title, content, completed, created_at, user_id) VALUES(?,?,?,?, ?)', 
                (title, content, False, now, user_id)
            )
            conn.commit()
        return "Task Created!!"  
    
    def update_task_completed(self, task_id):
        with get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE tasks SET completed = NOT completed WHERE id = ?', 
                (task_id,)
            )
            conn.commit()
        CustomDialog.show_info(self, "Task", "Updated task!!")
        self.create_task_cards()

    def delete_task(self, task_id):
        with get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            conn.commit()
        CustomDialog.show_info(self, "Task", "Deleted task!!")
        self.create_task_cards()
    
    def get_task_user(self):
        user = get_user(session.token)
        
        if user is None:
            return []
        
        with get_conn() as conn:
            cursor = conn.cursor()
            
            result = conn.execute(
                'SELECT id, title, content, completed FROM tasks WHERE user_id = ? ORDER BY created_at DESC', 
                (user[0], )
            ).fetchall()
            
        return result
    
    def logout(self):
        token = session.token
        
        if token:
            logout_user(token)
            self.controller.show_frame(login.LoginFrame)
        else:
            CustomDialog.show_info(self, "Logout", "Error Logout!!")     