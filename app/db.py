import os
from databases import Database

database: str = os.environ.get('DB_DATABASE')
user: str = os.environ.get('DB_USERNAME')
password: str = os.environ.get('DB_PASSWORD')
host: str = os.environ.get('DB_HOST')
port: int = os.environ.get('DB_PORT')

db = Database("sqlite+aiosqlite:///data.db")
