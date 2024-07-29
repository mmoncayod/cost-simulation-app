import streamlit as st
from msal import ConfidentialClientApplication
import settings

app = ConfidentialClientApplication(
    settings.CLIENT_ID,
    authority=settings.AUTHORITY,
    client_credential=settings.CLIENT_SECRET,
)

def authenticate_user():
    # Configuración de la base URL según el entorno
    base_url = "http://localhost:8501" if settings.environment == 'dev' else "https://cost-simulation-app-vthhaczahnv7bajvcnwnmj.streamlit.app"
    redirect_uri = f"{base_url}{settings.REDIRECT_PATH}"  # Asegúrate de que REDIRECT_PATH = '/getAToken'

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

# Llamar a esta función desde app.py para iniciar el proceso de autenticación
