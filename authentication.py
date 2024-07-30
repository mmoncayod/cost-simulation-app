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
    # get authorization code from URL
    query_params = st.query_params
    st.write("Query Params:", query_params) 
    code = query_params.get("code", [None])[0] # code is the authorization code sent by Azure AD after user authentication.
    st.write("Authorization Code:", code) # deactivate this ------its just for debuging --------

    if code and 'flow' in st.session_state:
        flow = st.session_state['flow']
        result = app.acquire_token_by_auth_code_flow(flow, {'code': code}, scopes=settings.SCOPES)
        if 'access_token' in result:
            st.session_state['authenticated'] = True
            st.session_state['user'] = result['account']
            st.success("Successfully logged in!")
            st.write("Access Token:", result['access_token']) # deactivate this ------its just for debuging --------
        else:
            st.error("Failed to log in.")
            st.write(result.get('error_description', ''))
    else:
        st.error("Authorization code not found in the request.")

