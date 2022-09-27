from pydantic import BaseSettings


class Settings(BaseSettings):
    db_host: str
    db_port: str
    db_user: str
    db_pwd: str
    db_name: str

    class Config:
        env_file = ".env"


settings = Settings()