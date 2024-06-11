import sqlite3
import os


DATABASE_NAME = os.path.abspath(os.path.join(os.path.dirname(__file__), 'magazine.db'))

def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn
    
