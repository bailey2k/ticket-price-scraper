#config file, don't touch

# pydantic allows for automatic checking, because who wants to manually check bad input
# takes our .env file and stores the input
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    email_from: str
    email_password: str
    smtp_server: str
    smtp_port: int 
    track_interval: int = 60
    mongo_url: str = 'mongodb://localhost:27017'

    class Config:
        env_file = ".env"

settings = Settings()