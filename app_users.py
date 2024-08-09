import streamlit as st
from streamlit_option_menu import option_menu
import authentication_users as authentication


def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )
    
    # Handle redirection from Azure AD
    if not "auth_uri" in st.session_state and ("authenticated" not in st.session_state or "flow" not in st.session_state):
        authentication.authenticate_user()

    if 'authenticated' not in st.session_state or not st.session_state.authenticated:
        st.warning("You are not logged in")
        st.stop()
    else:
        st.success(f"Welcome!")

    st.write("# Welcome to Streamlit! 👋")

    st.sidebar.success("Select a demo above.")

    st.markdown(
        """
        Streamlit is an open-source app framework built specifically for
        Machine Learning and Data Science projects.
        **👈 Select a demo from the sidebar** to see some examples
        of what Streamlit can do!
        ### Want to learn more?
        - Check out [streamlit.io](https://streamlit.io)
        - Jump into our [documentation](https://docs.streamlit.io)
        - Ask a question in our [community
          forums](https://discuss.streamlit.io)
        ### See more complex demos
        - Use a neural net to [analyze the Udacity Self-driving Car Image
          Dataset](https://github.com/streamlit/demo-self-driving)
        - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
        """
    )
    

run()
