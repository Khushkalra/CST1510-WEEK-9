import streamlit as st
from datetime import date
from app_backend.incidents import get_incidents, add_incident

#configure the streamlit page
st.set_page_config(page_title="Incidents", page_icon="🛡", layout="wide")

#stops access if the user is not logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must log in first.")
    st.stop()

st.title("Incident Management")
#create two tabs one for viewing incidents and one for adding new
tab1, tab2 = st.tabs(["View Incidents", "Add Incident"])

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