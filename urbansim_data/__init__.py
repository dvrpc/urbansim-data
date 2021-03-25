import os
from pathlib import Path
import platform

import pg_data_etl as pg
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

GDRIVE_FOLDER = Path(os.getenv("GOOGLE_DRIVE_ROOT"))

_db_credentials = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "un": os.getenv("DB_USER"),
    "pw": os.getenv("DB_PW"),
    "super_un": os.getenv("DB_SUPER_UN") or "postgres",
    "super_pw": os.getenv("DB_SUPER_PW") or os.getenv("DB_PW"),
}


_db = pg.Database(os.getenv("DB_NAME"), **_db_credentials)
