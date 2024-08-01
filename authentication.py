import streamlit as st
from msal import ConfidentialClientApplication
import settings

#--- // ---#
# Crear un cliente de autenticación utilizando MSAL (Microsoft Authentication Library)
# con la configuración proporcionada (ID de cliente, autoridad, secreto de cliente)
# Esto es esencial para interactuar con Azure AD y gestionar los tokens de acceso.

app = ConfidentialClientApplication(
    settings.CLIENT_ID,
    authority=settings.AUTHORITY,
    client_credential=settings.CLIENT_SECRET,
)

#--- // ---#
#  Iniciar el proceso de autenticación del usuario.

def authenticate_user():
    #  Define la URI de redirección a la que Azure AD enviará al usuario después de la autenticación.
    base_url = "http://localhost:8501" if settings.environment == 'dev' else "https://cost-simulation-app-vthhaczahnv7bajvcnwnmj.streamlit.app"
    redirect_uri = base_url  

    result = None # almacenara el token de acceso

    # Verifica si hay cuentas almacenadas y trata de adquirir un token en silencio 
    # (sin intervención del usuario) si ya hay una sesión activa
    #accounts = app.get_accounts()
    #if accounts:
        #result = app.acquire_token_silent(settings.SCOPES, account=accounts[0]) 

    # Si no hay token en la session se inicia el flujo de autenticacion
    #if not result:
    flow = app.initiate_auth_code_flow(settings.SCOPES, redirect_uri=redirect_uri)
    st.session_state["flow"] = flow
    st.session_state["auth_uri"] = flow["auth_uri"]
    st.session_state["state"] = flow["state"] 
    st.write("Flow initialized and stored in session:", flow) # ESTA PIDIENDO PERMISOS ADICIONALES? POR QUE?

#--- // ---#

def handle_redirect():
    # get authorization code from URL
    query_params = st.query_params
    st.write("Query Params:", query_params) 
    code = query_params.get("code", [None])[0] # this is ok -- code is the authorization code sent by Azure AD after user authentication.

    if code and 'flow' in st.session_state:
        flow = st.session_state['flow']
        st.write("Flow data", flow)
        try:
            result = app.acquire_token_by_auth_code_flow(flow, {'code': code}, scopes=settings.SCOPES)
            st.write("Result:", result)  # Debería mostrar el resultado del intercambio
            if 'access_token' in result:
                st.session_state['authenticated'] = True
                st.session_state['user'] = result.get('account')
                st.success("Successfully logged in!")
                st.write("Access Token:", result['access_token'])
            else:
                st.error("Failed to log in.")
                st.write(result.get('error_description', 'No error description available.'))
        except Exception as e:
            st.error("An exception occurred during token exchange.")
            st.write(str(e))
    else:
        st.error("Authorization code or flow not found in session.")

