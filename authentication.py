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
        result = app.acquire_token_silent(settings.SCOPES_AUTH, account=accounts[0]) # Authentication 

    if not result:
        flow = app.initiate_auth_code_flow(settings.SCOPES_AUTH, redirect_uri=redirect_uri)
        st.session_state["flow"] = flow
        st.session_state["auth_uri"] = flow["auth_uri"]
        st.write("Flow initialized and stored in session:", flow) 

def handle_redirect():
    # get authorization code from URL
    query_params = st.query_params
    st.write("Query Params:", query_params) 
    code = query_params.get("code", [None])[0] # this is ok -- code is the authorization code sent by Azure AD after user authentication.

    if code and 'flow' in st.session_state:
        flow = st.session_state['flow']
        st.write("Flow data", flow)
        try:
            result = app.acquire_token_by_auth_code_flow(flow, {'code': code}, scopes=settings.SCOPES_AUTH)
            st.write("Result:", result)  # Debería mostrar el resultado del intercambio
            if 'access_token' in result:
                st.session_state['authenticated'] = True
                st.session_state['user'] = result.get('account')
                st.success("Successfully logged in!")
                st.write("Access Token:", result['access_token'])
                api_result = app.acquire_token_silent(scopes=settings.SCOPES_API, account=result['account'])
                if not api_result:
                    api_result = app.acquire_token_by_auth_code_flow(flow, {'code': code}, scopes=settings.SCOPES_API)
                st.write("API Access Token:", api_result.get('access_token', 'No token obtained'))
            else:
                st.error("Failed to log in.")
                st.write(result.get('error_description', 'No error description available.'))
        except Exception as e:
            st.error("An exception occurred during token exchange.")
            st.write(str(e))
    else:
        st.error("Authorization code or flow not found in session.")

