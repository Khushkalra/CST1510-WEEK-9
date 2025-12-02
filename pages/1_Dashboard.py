import streamlit as st
import pandas as pd
from app_backend.incidents import get_incidents
from app_backend.tickets import get_tickets
from app_backend.datasets import get_datasets

#configure Streamlit page settings
st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

#if user is not logged in, stop the dashboard from loading
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must log in first.")
    st.stop()

st.title("Dashboard")

#fetch incidents, tickets, and datasets from your backend service
incidents_df = get_incidents()
tickets_df = get_tickets()
datasets_df = get_datasets()

#show quick stats at the top (count of incidents, tickets, datasets)
col1, col2, col3 = st.columns(3)
col1.metric("Total Incidents", len(incidents_df))
col2.metric("Total Tickets", len(tickets_df))
col3.metric("Total Datasets", len(datasets_df))

st.write("---")

#check for column existence and non empty dataframe to avoid errors
st.subheader("Incidents by Severity")
if "severity" in incidents_df.columns and not incidents_df.empty:
    st.bar_chart(incidents_df["severity"].value_counts())
else:
    st.info("No severity data available.")

#tickets status chart
st.subheader("Tickets by Status")
if "status" in tickets_df.columns and not tickets_df.empty:
    st.bar_chart(tickets_df["status"].value_counts())
else:
    st.info("No ticket status data available.")

#datasets source chart
st.subheader("Datasets by Source")
if "source" in datasets_df.columns and not datasets_df.empty:
    st.bar_chart(datasets_df["source"].value_counts())
else:
    #message shown when no source column/data exists
    st.info("No dataset source data available.")