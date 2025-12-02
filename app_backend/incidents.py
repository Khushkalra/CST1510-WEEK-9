import pandas as pd
from app_backend.db import get_connection

def get_incidents():
    #return all cyber incidents as a DataFrame
    conn = get_connection()
    try:
        df = pd.read_sql("SELECT * FROM cyber_incidents", conn)
        return df
    finally:
        conn.close()

def add_incident(date_reported, incident_type, severity, status, description, reported_by):
    #insert a new incident into the cyber_incidents table
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO cyber_incidents
            (date_reported, incident_type, severity, status, description, reported_by)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (date_reported, incident_type, severity, status, description, reported_by),
        )
        conn.commit()
        return True
    except Exception as e:
        print("Error inserting incident:", e)
        return False
    finally:
        conn.close()