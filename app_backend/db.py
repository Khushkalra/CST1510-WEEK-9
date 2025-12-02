import sqlite3
from pathlib import Path

DB_PATH = Path("/Users/kk/Desktop/week8/DATA/intelligence_platform.db")

def get_connection():
    #create and return a new database connection
    return sqlite3.connect(DB_PATH)