import pandas as pd
from app_backend.db import get_connection

def get_datasets():
    #return all dataset metadata as a DataFrame
    conn = get_connection()
    try:
        df = pd.read_sql("SELECT * FROM datasets_metadata", conn)
        return df
    finally:
        conn.close()