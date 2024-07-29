import streamlit as st
from msal import ConfidentialClientApplication
import settings

app = ConfidentialClientApplication(
    settings.CLIENT_ID,
    authority=settings.AUTHORITY,
    client_credential=settings.CLIENT_SECRET,
)

def authenticate_user():
    base_url = "https://cost-simulation-app-vthhaczahnv7bajvcnwnmj.streamlit.app" if settings.environment == 'prod' else "http://localhost:8501"
    redirect_uri = f"{base_url}{settings.REDIRECT_PATH}"  

    result = None
    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(settings.SCOPES, account=accounts[0])

    if not result:
        flow = app.initiate_auth_code_flow(settings.SCOPES, redirect_uri=redirect_uri)
        st.write('Please log in:', flow['auth_uri'])

    if result:
        st.write("Successfully logged in!")
        st.write(result['account']['username'])
    else:
        st.write("Please log in to see your username.")

