import dataclasses
import os
import typing
from dataclasses import dataclass
from pathlib import Path
from typing import Union, Optional

from dotenv import dotenv_values

# replace with dynaconf 4.0 when released
# maybe replace .env with toml
from starlette.templating import Jinja2Templates

acceptable_number = Union[int, None]


@dataclass
class Setting:
    app_host: str = "127.0.0.1"
    app_port: int = 5000
    database_url: str = ""
    redoc_url: Optional[str] = "/redoc"
    docs_url: Optional[str] = "/docs"
    openapi_url: Optional[str] = "/openapi.json"

    def __post_init__(self):

        for field in dataclasses.fields(self):
            value = getattr(self, field.name)
            if not isinstance(value, field.type):
                if field.type is str and value is not None:
                    value = str(value)
                elif field.type is int and value is not None:
                    value = int(value)
                elif field.type is bool and value is not None:
                    value = bool(value)
                elif field.type is acceptable_number and value is not None:
                    value = int(value)
                setattr(self, field.name, value)
            if field.type is typing.Optional[str] and value == "" or value == "None":
                setattr(self, field.name, None)


current_path = os.path.dirname(os.path.abspath(__file__))
project_path = Path(current_path).parent
dotenv_con = dotenv_values(project_path.joinpath(".env"))
templates = Jinja2Templates(directory=project_path / "templates")
setting: Setting = Setting(**dotenv_con)
