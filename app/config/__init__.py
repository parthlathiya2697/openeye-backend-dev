from distutils.debug import DEBUG
import os
import configparser
import configparser
from pathlib import Path
from dotenv import load_dotenv
from typing import  Optional, List, Union
from pydantic import AnyHttpUrl, BaseSettings, validator, PostgresDsn

path = Path(os.path.dirname(__file__))
BASE_DIR = str(path.parent)  #/app

# Load environment variables
env_path = os.path.join(Path(BASE_DIR).parent, '.env')
load_dotenv( dotenv_path= env_path )

# Load environment variables
env_path = os.path.join(Path(BASE_DIR).parent, '.env')
load_dotenv( dotenv_path= env_path )

config = configparser.ConfigParser()
config.read( os.path.join(BASE_DIR, "config", "settings.ini"))

class Settings(BaseSettings):

    PROJECT_NAME: str = "Vision Docs"
    PROJECT_DESCRIPTION: str = "Vision's API document. Register an account and Use the API. register an account. Contact us at vision.on.ai@gmail.com"
    ADMIN_EMAIL: str = "vision.on.ai@gmail.com"
    DEBUG: bool = os.getenv("DEBUG")

    # Server
    SERVER_NAME: Optional[str]
    SERVER_HOST: Optional[AnyHttpUrl]
    SENTRY_DSN: Optional[str]
    SECRET_KEY: bytes = os.urandom(32)
    TERMS_OF_SERVICE: str = "<link to services page>"

    PROJECT_VERSION: str = "v1"
    API_V1_STR: str = f'/{PROJECT_VERSION}'

    if os.getenv('ENV') and os.getenv('ENV') == "DEVELOPMENT":
        BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost.tiangolo.com", "https://localhost.tiangolo.com", "http://localhost", "http://localhost:8080"]
    else:
        BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    def assemble_db_connection(self):
        return PostgresDsn.build(
            scheme="postgresql",
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_SERVER"),
            path=f'{os.getenv("POSTGRES_DB") or ""}',
        )

# Create an Object to use across the project
settings = Settings()