import streamlit as st
from msal import ConfidentialClientApplication
import settings

app = ConfidentialClientApplication(
    settings.CLIENT_ID,
    authority=settings.AUTHORITY,
    client_credential=settings.CLIENT_SECRET,
)

def authenticate_user():
    base_url = "http://localhost:8501" if settings.environment == 'dev' else "https://cost-simulation-app-vthhaczahnv7bajvcnwnmj.streamlit.app"
    redirect_uri = base_url  

    result = None
    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(settings.SCOPES, account=accounts[0]) # Get a token without user intervention

    if not result:
        flow = app.initiate_auth_code_flow(settings.SCOPES, redirect_uri=redirect_uri)
        st.session_state["flow"] = flow
        st.session_state["auth_uri"] = flow["auth_uri"]

def handle_redirect():
    query_params = st.query_params
    st.write("Query Params:", query_params)  # Mostrar todos los parámetros para depuración

    # Verificar si 'code' está en los parámetros y extraer el primer valor si es una lista
    code_list = query_params.get("code", [None])
    code = code_list[0] if code_list else None

    st.write("Authorization Code:", code)  # Mostrar el código para depuración

    if code and code != "0":  # Asegúrate de que el código es válido y no '0'
        if 'flow' in st.session_state:
            flow = st.session_state['flow']
            result = app.acquire_token_by_auth_code_flow(flow, {'code': code}, scopes=settings.SCOPES)
            if 'access_token' in result:
                st.session_state['authenticated'] = True
                st.session_state['user'] = result['account']
                st.success("Successfully logged in!")
                st.write("Access Token:", result['access_token'])  # Para depuración
            else:
                st.error("Failed to log in.")
                st.write(result.get('error_description', ''))
        else:
            st.error("Flow not found in session state.")
    else:
        st.error("Authorization code not found or is invalid in the request.")

