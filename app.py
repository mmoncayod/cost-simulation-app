import streamlit as st
from streamlit_option_menu import option_menu
from pages import page1, page2, page3
import authentication
import time
import settings
import msal


def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

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

if __name__ == "__main__":
    run()

# start the application MSAL
app = msal.ConfidentialClientApplication(
    client_id=settings.CLIENT_ID,
    client_credential=settings.CLIENT_SECRET,
    authority=settings.AUTHORITY
)

# verify roles
def has_role(token_claims, role):
    return role in token_claims.get('roles', [])

# auth_token, refresh_token,token_expiry are in the streamlit session? if not initialize as None (it means they don't have value yet)
if "auth_token" not in st.session_state:
    st.session_state.auth_token = None
    st.session_state.refresh_token = None
    st.session_state.token_expiry = None

# Token has expired?
if st.session_state.auth_token:
    if time.time() > st.session_state.token_expiry:
        st.write("Your token has expired, renewing...")
        token_response = authentication.refresh_token(st.session_state.refresh_token)
        if "access_token" in token_response:
            st.session_state.auth_token = token_response["access_token"]
            st.session_state.token_expiry = time.time() + token_response["expires_in"]
        else:
            st.error("Error renewing the token, please log in again.")
            st.session_state.auth_token = None
            st.session_state.refresh_token = None
            st.session_state.token_expiry = None

# If the user is not logged in, show link to log in
if st.session_state.auth_token is None:
    st.write("Please sign in with Azure AD.")
    auth_url = authentication.get_auth_url()
    st.write(f"[sign in with Azure AD]({auth_url})")
else:
    st.write("You are already logged in.")
    st.write("Access token:", st.session_state.auth_token)

# Manejar la redirección de Azure AD con el código de autorización
query_params = st.query_params
if "code" in query_params:
    callback_url = query_params["code"][0]
    token_response = authentication.get_token_from_code(callback_url)
    if "access_token" in token_response:
        st.session_state.auth_token = token_response["access_token"]
        st.session_state.refresh_token = token_response["refresh_token"]
        st.session_state.token_expiry = time.time() + token_response["expires_in"]
        st.experimental_rerun()
    else:
        st.error("Authentication error.")