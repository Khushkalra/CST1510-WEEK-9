import pandas as pd
from app_backend.db import get_connection

def get_incidents():
    #return all cyber incidents as a DataFrame
    conn = get_connection()
    try:
        df = pd.read_sql(
            """
            SELECT
                rowid AS incident_id,
                date_reported,
                incident_type,
                severity,
                status,
                description,
                reported_by
            FROM cyber_incidents
            """,
            conn
        )
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

def delete_incident(incident_id: int) -> bool:
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM cyber_incidents WHERE rowid = ?", (incident_id,))

        conn.commit()
        conn.close()

        return cursor.rowcount > 0

    except Exception as e:
        print("Error deleting incident:", e)
        return False