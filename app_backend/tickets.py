import pandas as pd
from app_backend.db import get_connection

def get_tickets():
    #return all IT tickets as a DataFrame
    conn = get_connection()
    try:
        df = pd.read_sql("SELECT * FROM it_tickets", conn)
        return df
    finally:
        conn.close()