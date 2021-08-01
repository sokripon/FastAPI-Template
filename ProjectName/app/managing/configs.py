from pathlib import Path

import toml
from pydantic import BaseModel


class GeneralSettings(BaseModel):
    project_name: str
    mode: str = "dev"
    hostname: str
    port: int = 8761
    reload: bool = True
    database: bool = False


class DatabaseSettings(BaseModel):
    dbms: str
    host: str
    name: str
    username: str
    password: str


class Settings:
    database: DatabaseSettings
    general: GeneralSettings

    def __init__(self):
        self._load_from_toml()

    def _load_from_toml(self):
        toml_settings = toml.load(f"{Path(__file__).parent.parent.parent}/config.toml")

        self.database = DatabaseSettings(**(toml_settings.get("database")))
        self.general = GeneralSettings(**(toml_settings.get("general")))


settings = Settings()
