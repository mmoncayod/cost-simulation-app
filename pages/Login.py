import streamlit as st
import authentication

def login_page():
    st.title("Login")

    if "auth_uri" in st.session_state:
        st.markdown(f"[Log in with Microsoft]({st.session_state['auth_uri']})")
    else:
        authentication.authenticate_user()
        if "auth_uri" in st.session_state:
            st.markdown(f"[Log in with Microsoft]({st.session_state['auth_uri']})")
