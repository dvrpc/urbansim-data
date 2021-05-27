import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

from pg_data_etl import Database


load_dotenv(find_dotenv())

GDRIVE_FOLDER = Path(os.getenv("GOOGLE_DRIVE_ROOT"))

_credentials = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "un": os.getenv("DB_USER"),
    "pw": os.getenv("DB_PW"),
    "super_un": os.getenv("DB_SUPER_UN") or "postgres",
    "super_pw": os.getenv("DB_SUPER_PW") or os.getenv("DB_PW"),
}

_db_name = os.getenv("DB_NAME")

_db = Database.from_parameters(_db_name, **_credentials)
