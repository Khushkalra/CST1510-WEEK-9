import pandas as pd
from app_backend.db import get_connection

# =========================
# GET ALL TICKETS
# =========================
def get_tickets():
    conn = get_connection()
    try:
        df = pd.read_sql(
            """
            SELECT 
                ticket_id,
                date_created,
                priority,
                status,
                description,
                COALESCE(assigned_to, 'Unassigned') AS assigned_to
            FROM it_tickets
            ORDER BY date_created DESC
            """,
            conn
        )
        return df
    finally:
        conn.close()


# =========================
# ADD NEW TICKET
# =========================
def add_ticket(ticket_id, date_created, priority, status, description, assigned_to):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO it_tickets 
            (ticket_id, date_created, priority, status, description, assigned_to)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (ticket_id, date_created, priority, status, description, assigned_to)
        )
        conn.commit()
        return True
    except Exception as e:
        print("ADD ERROR:", e)
        return False
    finally:
        conn.close()


# =========================
# DELETE TICKET
# =========================
def delete_ticket(ticket_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM it_tickets WHERE ticket_id = ?", (ticket_id,))
        conn.commit()
        return cur.rowcount > 0
    finally:
        conn.close()


# =========================
# GET SPECIFIC TICKET
# =========================
def get_ticket_by_id(ticket_id):
    conn = get_connection()
    try:
        df = pd.read_sql(
            "SELECT * FROM it_tickets WHERE ticket_id = ?",
            conn,
            params=[ticket_id],
        )

        if df.empty:
            return None

        return df.iloc[0].to_dict()

    finally:
        conn.close()


# =========================
# UPDATE A TICKET
# =========================
def update_ticket(ticket_id, priority, status, description, assigned_to):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE it_tickets
            SET priority = ?, status = ?, description = ?, assigned_to = ?
            WHERE ticket_id = ?
            """,
            (priority, status, description, assigned_to, ticket_id),
        )
        conn.commit()
        return True
    except Exception as e:
        print("UPDATE ERROR:", e)
        return False
    finally:
        conn.close()
