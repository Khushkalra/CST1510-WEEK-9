import streamlit as st
from datetime import date
from app_backend.incidents import get_incidents, add_incident, delete_incident

#configure the streamlit page
st.set_page_config(page_title="Incidents", page_icon="🛡", layout="wide")

#stops access if the user is not logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must log in first.")
    st.stop()

st.title("Incident Management")
#create two tabs one for viewing incidents and one for adding new
tab1, tab2,tab3 = st.tabs(["View Incidents", "Add Incident", "Delete Incident"])

with tab1:
    st.subheader("All Incidents")
    df = get_incidents()
    st.dataframe(df, use_container_width=True)

with tab2:
    st.subheader("Add New Incident")

    inc_date = st.date_input("Date Reported", date.today())
    inc_type = st.text_input("Incident Type")
    severity = st.selectbox("Severity", ["Low", "Medium", "High"])
    status = st.selectbox("Status", ["Open", "Closed"])
    desc = st.text_area("Description")
    #button to save a new incident
    if st.button("Save Incident"):
        #get username from session or default to "system"
        username = st.session_state.get("username", "system")
        ok = add_incident(
            inc_date.isoformat(),
            inc_type,
            severity,
            status,
            desc,
            username,
        )
        if ok:
            st.success("Incident added.")
        else:
            st.error("Failed to add incident.")
with tab3:
    st.subheader("Delete Incident")

    df = get_incidents()

    if df.empty:
        st.info("No incidents available to delete.")
    else:
        #we already know the ID column name
        id_col = "incident_id"

        # Input box instead of dropdown
        incident_id_input = st.number_input(
            "Enter Incident ID to delete",
            min_value=1,
            step=1
        )

        #delete button
        if st.button("Delete Incident"):
            # Check if ID exists
            if incident_id_input not in df[id_col].values:
                st.error(f"Incident ID {incident_id_input} does not exist.")
            else:
                if delete_incident(int(incident_id_input)):
                    st.success(f"Incident {incident_id_input} deleted successfully.")
                else:
                    st.error("Failed to delete incident.")
