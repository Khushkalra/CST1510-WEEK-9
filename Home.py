import streamlit as st
from app_backend.users import register_user, login_user
#configure streamlit page
st.set_page_config(page_title="Cyber Platform - Login")

#initialize session state variables for login tracking
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

st.title("Cyber Intelligence Platform")

#dropdown box for choosing between Login and Register
menu = ["Login", "Register"]
choice = st.selectbox("Select Option", menu)

if choice == "Login":
    st.subheader("Login")

    #input field for existing user
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        #check credentials using backend function
        success, message = login_user(username, password)
        if success:
            #set session details to keep user logged in across pages
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login successful!")
            #redirect to dashboard page
            st.switch_page("pages/1_Dashboard.py")
        else:
            st.error(message)
#register section
else:
    st.subheader("Register")

    new_user = st.text_input("New Username")
    new_pass = st.text_input("New Password", type="password")

    if st.button("Register"):
        success, message = register_user(new_user, new_pass)
        if success:
            st.success("User registered. You can now log in.")
        else:
            st.error(message)