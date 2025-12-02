import streamlit as st
from app_backend.incidents import get_incidents
from app_backend.tickets import get_tickets
from app_backend.datasets import get_datasets
#configure streamlit page details
st.set_page_config(page_title="Data Explorer", page_icon="📂", layout="wide")

#prevent access if user is not logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must log in first.")
    st.stop()

st.title("Data Explorer")
#create tabs for different types of data
tab1, tab2, tab3 = st.tabs(["Cyber Incidents", "IT Tickets", "Datasets Metadata"])

#cyber incidents tab
with tab1:
    st.subheader("Cyber Incidents")
    st.dataframe(get_incidents(), use_container_width=True)

#IT ticket tab
with tab2:
    st.subheader("IT Tickets")
    st.dataframe(get_tickets(), use_container_width=True)

#datasets metadata tab
with tab3:
    st.subheader("Datasets Metadata")
    st.dataframe(get_datasets(), use_container_width=True)