import streamlit as st
from datetime import date
from app_backend.tickets import (
    get_tickets,
    add_ticket,
    delete_ticket,
    get_ticket_by_id,
    update_ticket
)

st.title("IT Ticket Management")

tab1, tab2, tab3, tab4 = st.tabs(["View Tickets", "Add Ticket", "Update Ticket", "Delete Ticket"])

# =========================
# VIEW TICKETS
# =========================
with tab1:
    st.subheader("All Tickets")
    st.dataframe(get_tickets(), use_container_width=True)

# =========================
# ADD TICKET
# =========================
with tab2:
    st.subheader("Create New Ticket")

    ticket_id = st.text_input("Ticket ID (e.g., TICKET_1010)")
    date_created = st.date_input("Date Created", date.today()).isoformat()
    priority = st.selectbox("Priority", ["Low", "Medium", "High", "None"], index=3)
    status = st.selectbox("Status", ["Open", "Closed"])
    description = st.text_area("Description")
    assigned_to = st.text_input("Assigned To (Optional)", value="Unassigned")

    if st.button("Add Ticket"):
        if add_ticket(ticket_id, date_created, priority, status, description, assigned_to):
            st.success("Ticket added successfully!")
        else:
            st.error("Failed to add ticket.")

# =========================
# UPDATE TICKET
# =========================
# ---------------------- UPDATE TICKET TAB ----------------------
# ---------------------- UPDATE TICKET TAB ----------------------
with tab3:
    st.subheader("Update Ticket")

    df = get_tickets()

    if df.empty:
        st.info("No tickets available to update.")
    else:
        ticket_ids = df["ticket_id"].tolist()

        # Select ticket
        selected_ticket_id = st.selectbox("Select Ticket to Update", ticket_ids, key="select_ticket_update")

        # Load ticket data
        ticket_data = get_ticket_by_id(selected_ticket_id)

        if ticket_data:
            st.write("### Current Ticket Details")
            st.json(ticket_data)

            # ---------------- Priority ----------------
            priority_options = ["Low", "Medium", "High", "None"]
            current_priority = (
                ticket_data["priority"]
                if ticket_data["priority"] in priority_options
                else "None"
            )

            new_priority = st.selectbox(
                "Priority",
                priority_options,
                index=priority_options.index(current_priority),
                key="update_priority"
            )

            # ---------------- Status ----------------
            status_options = ["Open", "Closed"]
            current_status = (
                ticket_data["status"]
                if ticket_data["status"] in status_options
                else "Open"
            )

            new_status = st.selectbox(
                "Status",
                status_options,
                index=status_options.index(current_status),
                key="update_status"
            )

            # ---------------- Description ----------------
            new_description = st.text_area(
                "Description",
                value=ticket_data["description"] if ticket_data["description"] else "",
                key="update_description"
            )

            # ---------------- Assigned To ----------------
            new_assigned_to = st.text_input(
                "Assigned To",
                value=ticket_data["assigned_to"] if ticket_data["assigned_to"] else "Unassigned",
                key="update_assigned_to"
            )

            # ---------------- Save Button ----------------
            if st.button("Save Changes", key="update_button"):
                ok = update_ticket(
                    selected_ticket_id,
                    new_priority,
                    new_status,
                    new_description,
                    new_assigned_to,
                )

                if ok:
                    st.success(f"Ticket {selected_ticket_id} updated successfully!")
                else:
                    st.error("Failed to update ticket.")


# =========================
# DELETE TICKET
# =========================
with tab4:
    st.subheader("Delete a Ticket")

    df = get_tickets()
    if df.empty:
        st.info("No tickets available.")
    else:
        ticket_ids = df["ticket_id"].tolist()
        delete_id = st.selectbox("Select Ticket to Delete", ticket_ids)

        if st.button("Delete Ticket"):
            if delete_ticket(delete_id):
                st.success(f"Ticket {delete_id} deleted.")
            else:
                st.error("Failed to delete ticket.")
