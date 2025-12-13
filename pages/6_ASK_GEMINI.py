import streamlit as st
import google.generativeai as genai

st.title("💬 ASK GEMINI")

# Load API key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-2.5-flash")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Get input FIRST
prompt = st.chat_input("Say something...")

if prompt:
    # Save + display user
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Gemini response
    response = model.generate_content(prompt).text

    # Save assistant message
    st.session_state.messages.append({"role": "assistant", "content": response})

# NOW display entire chat history (after updates)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
