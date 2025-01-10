import os

from dotenv import load_dotenv

load_dotenv()


class SQLiteDAOBase:
    DB_NAME: str = os.environ["SQLITE_DB_NAME"]
