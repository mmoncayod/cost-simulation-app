import streamlit as st
import authentication

if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.error("Please log in to access this page.")
    st.stop()

st.write(f"Welcome, {st.session_state['user']['username']}!")

def show():
    st.title('This is page 1')
    st.write('This is the content for page 1')


