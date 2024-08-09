import streamlit as st
from msal import ConfidentialClientApplication, ClientApplication
import settings
import webbrowser

#--- // ---#
# Create a authentication client using MSAL (Microsoft Authentication Library)
# with the provided configuration (client_it, tenant, client_secret)
# This is essential to interact with Azure AD and manage access tokens

#--- // ---#
#  Iniciar el proceso de autenticación del usuario.

def authenticate_user():
    # Get the session to connect to the Microsoft App.
  
    app = ConfidentialClientApplication(
        settings.CLIENT_ID,
        authority=settings.AUTHORITY,
        client_credential=settings.CLIENT_SECRET,
    )

    
    #  Define la URI de redirección a la que Azure AD enviará al usuario después de la autenticación.
    base_url = "http://localhost:8501" if settings.environment == 'dev' else "https://cost-simulation-app-vthhaczahnv7bajvcnwnmj.streamlit.app"
    redirect_uri = base_url  

    result = None # almacenara el token de acceso


    accounts = app.get_accounts()
    try:
        # Check for stored accounts and try to silently acquire a token
        if accounts:
            result = app.acquire_token_silent(settings.SCOPES, account=accounts[0]) 
        # If there is no token in the session, the authentication flow starts
        # flow: Contains information necessary to complete the authentication flow(state, redirect_uri, scope, auth_uri, code_verifier, nonce, claims_challenge)

        if not result:
            flow = app.initiate_auth_code_flow(settings.SCOPES, redirect_uri=redirect_uri)
            st.session_state["flow"] = flow
            st.session_state["auth_uri"] = flow["auth_uri"]
            st.session_state["state"] = flow["state"]
            st.write("session state", st.session_state)
            webbrowser.open(st.session_state['auth_uri'], new=2, autoraise=True)
            query_params = st.query_params
            code = query_params["code"] if "code" in query_params else None

        if "code" in query_params:
            state = query_params["state"] if "state" in query_params else None
            st.write("session state 2", st.session_state)
            flow = st.session_state.get("flow", None)


            if not code or not state:
                st.error("Authorization code or state is missing.")
                return

            if not flow:
                st.error("flow is missing.")
                return


            try:
                result = app.acquire_token_by_authorization_code(
                    code,  # El código de autorización obtenido
                    scopes=settings.SCOPES,  # Los alcances que solicitaste
                    redirect_uri=redirect_uri  # La misma URI de redirección utilizada en el flujo de solicitud inicial
                )
                if "access_token" in result:
                    st.session_state["authenticated"] = True
                    st.session_state["token"] = result
                    st.success("Authentication successful!")
                    return
                else:
                    st.error(f"Failed to acquire tokens: {result.get('error_description')}")
                    return
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.error("")
    except Exception as e:
        print(e)
    
    return st.session_state 

    # Until here we get the flow, the code to exchange with the access token
    # but we get the error repsonse “Failed to acquire 
    # tokens: AADSTS50148: The code_verifier does not match the code_challenge 
    # supplied in the authorization request for PKCE”