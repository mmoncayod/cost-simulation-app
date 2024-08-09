import streamlit as st
from msal import ConfidentialClientApplication, ClientApplication
import settings
import webbrowser

#--- // ---#
# Create a authentication client using MSAL (Microsoft Authentication Library)
# with the provided configuration (client_it, tenant, client_secret)
# This is essential to interact with Azure AD and manage access tokens

#--- // ---#
#  Start the user authentication process

def authenticate_user():
    # Get the session to connect to the Microsoft App.
    input_secret = st.text_input('Please provide us your secret')
    

    app = ConfidentialClientApplication(
        settings.CLIENT_ID,
        authority=settings.AUTHORITY,
        client_credential=input_secret,
    )
    
    #  Defines the redirect URI that Azure AD will send the user to after authentication.
    base_url = "http://localhost:8501" if settings.environment == 'dev' else "https://cost-simulation-app-vthhaczahnv7bajvcnwnmj.streamlit.app"
    redirect_uri = base_url  

    result = None # will store the access token


    accounts = app.get_accounts()
    try:
        # Check for stored accounts and try to silently acquire a token
        if accounts:
            result = app.acquire_token_silent(settings.SCOPES, account=accounts[0]) 
        # If there is no token in the session, the authentication flow starts
        # flow: Contains information necessary to complete the authentication flow(state, redirect_uri, scope, auth_uri, code_verifier, nonce, claims_challenge)
        if not result:
            token_result = app.acquire_token_silent(['https://graph.microsoft.com/.default'], account=None)
            #access_token = 'Bearer ' + token_result['access_token']
            if token_result:
                print('Access token was loaded from cache')

        if not token_result or not input:
            token_result = app.acquire_token_for_client(scopes=['https://graph.microsoft.com/.default'])
            #access_token = 'Bearer ' + token_result['access_token']
            if token_result:
                print('New access token was acquired from Azure AD')

            if "access_token" in token_result:
                st.session_state["authenticated"] = True
                st.session_state["token"] = result
                st.success("Authentication successful!")
                return
            else:
                st.error(f"Failed to acquire tokens: {result.get('error_description')}")
                return
    except Exception as e:
        print(e)
    
    
    # This app work with Authentication client, managing the user login with 
    # secret clients into the Azure app