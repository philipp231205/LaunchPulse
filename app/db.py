import os
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()
DB_CONNECTION = os.getenv("DATABASE_URL")

def get_conn():
	return psycopg.connect(DB_CONNECTION, row_factory = dict_row)