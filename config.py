from pydantic_settings import BaseSettings
from dotenv import load_dotenv


load_dotenv()

class Settings(BaseSettings):
    db_path : str
    secret_key_jwt: str
    algorithm: str
    session_filename : str

    class Config:
        env_file = ".env"

settings = Settings()