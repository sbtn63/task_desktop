import os
import pickle

from config import settings

class Session:
    def __init__(self):
        self.token = None
        self.username = None
        self.filename = settings.session_filename

    def save_session(self):
        with open(self.filename, 'wb') as file:
            pickle.dump({'token': self.token, 'username': self.username}, file)

    def load_session(self):
        try:
            with open(self.filename, 'rb') as file:
                data = pickle.load(file)
                self.token = data['token']
                self.username = data['username']
                return True
        except FileNotFoundError:
            return False
    
    def delete_file_session(self):
        try:
            os.remove(self.filename)
            print(f"Archivo {self.filename} eliminado correctamente.")
        except FileNotFoundError:
            print(f"El archivo {self.filename} no existe.")

session = Session()
