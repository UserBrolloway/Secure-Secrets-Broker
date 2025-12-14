from pydantic import BaseSettings

class Settings(BaseSettings):
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    database_url: str
    vault_addr: str = "http://localhost:8200"
    vault_token: str = "root"
    admin_api_key: str = "changeme"

    class Config:
        env_file = ".env"

settings = Settings()
