import streamlit as st
from app_backend.users import register_user, login_user
#configure streamlit page
st.set_page_config(page_title="Cyber Platform - Login", layout="wide")

#initialize session state variables for login tracking
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

st.markdown(
    """
    <div style="
        background: linear-gradient(90deg, #0f2027, #203a43, #2c5364);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 40px;
        font-weight: 700;
        color: #00f0ff;
        text-shadow:
            0 0 5px #FF3131,
            0 0 10px #00f0ff,
            0 0 29px #FF3131,
            0 0 20px #00cfff;
    ">
        CYBER INTELLIGENCE PLATFORM
    </div>
    """,unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1614064641938-3bbee52942c7");
        background-size: cover;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)

#dropdown box for choosing between Login and Register
col1, _, col2 = st.columns([1, 0.1, 1])

with col1:
    if st.button("🔐 Login"):
        st.session_state.choice = "Login"

with col2:
    if st.button("📝 Register"):
        st.session_state.choice = "Register"

choice = st.session_state.get("choice", "Login")

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
st.sidebar.title("🛡️ Cyber Platform")
st.sidebar.caption("--------------------BE SAFE---------------------")
st.sidebar.image("/Users/kk/Desktop/1.jpeg", width=350)