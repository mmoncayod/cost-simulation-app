import streamlit as st
from msal import ConfidentialClientApplication
import settings

# Utilizar las configuraciones desde settings.py
app = ConfidentialClientApplication(
    settings.CLIENT_ID,
    authority=settings.AUTHORITY,
    client_credential=settings.CLIENT_SECRET,
)

def authenticate_user():
    result = None
    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(settings.SCOPES, account=accounts[0])

    if not result:
        flow = app.initiate_auth_code_flow(settings.SCOPES, redirect_uri="http://localhost:8501" + settings.REDIRECT_PATH)
        st.write('Please log in:', flow['auth_uri'])

    if result:
        st.write("Successfully logged in!")
        st.write(result['account']['username'])
    else:
        st.write("Please log in to see your username.")

# Esta función puede ser llamada en app.py para iniciar el proceso de autenticación
