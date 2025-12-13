import pandas as pd
from app_backend.db import get_connection


def get_datasets():
    conn = get_connection()
    try:
        df = pd.read_sql(
            """
            SELECT 
                rowid AS id,
                dataset_name,
                source,
                record_count,
                last_updated,
                description
            FROM datasets_metadata
            """,
            conn
        )
        return df
    finally:
        conn.close()

def add_dataset(name, source, record_count, last_updated, description):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO datasets_metadata
            (dataset_name, source, record_count, last_updated, description)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, source, record_count, last_updated, description)
        )
        conn.commit()
        return True
    except Exception as e:
        print("ADD DATASET ERROR:", e)
        return False
    finally:
        conn.close()


def get_dataset_by_id(dataset_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            rowid AS id,
            dataset_name,
            source,
            record_count,
            last_updated,
            description
        FROM datasets_metadata
        WHERE rowid = ?
    """, (dataset_id,))

    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    columns = ["id", "dataset_name", "source", "record_count", "last_updated", "description"]
    return dict(zip(columns, row))

def update_dataset(dataset_id, dataset_name, source, record_count, last_updated, description):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE datasets_metadata
        SET 
            dataset_name = ?,
            source = ?,
            record_count = ?,
            last_updated = ?,
            description = ?
        WHERE rowid = ?
    """, (dataset_name, source, record_count, last_updated, description, dataset_id))

    conn.commit()
    conn.close()
    return True

def delete_dataset(dataset_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM datasets_metadata WHERE rowid = ?", (dataset_id,))
    conn.commit()
    conn.close()
    return True
