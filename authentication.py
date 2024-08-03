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
    base_url = "http://localhost:8501" if settings.environment == 'dev' else "https://cost-simulation-app-vthhaczahnv7bajvcnwnmj.streamlit.app"
    redirect_uri = base_url

    # Obtener parámetros de la URL
    query_params = st.query_params
    code = query_params["code"] if "code" in query_params else None
    state = query_params["state"] if "state" in query_params else None  

    # Si no hay token en la sesión se inicia el flujo de autenticación
    result = None
    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(settings.SCOPES, account=accounts[0])

    if not result:
        flow = app.initiate_auth_code_flow(settings.SCOPES, redirect_uri=redirect_uri)
        st.session_state["flow"] = flow
        st.session_state["auth_uri"] = flow["auth_uri"]
        st.session_state["state"] = flow["state"]
        #st.write("Flow initialized and stored in session:", flow)

    # Manejar redirección si el código de autorización está presente
    if code and state:
        #st.write("Authorization Code:", code)
        #st.write("State:", state)
        
        if "flow" in st.session_state:
            flow = st.session_state["flow"]
            st.write("Flow in handle redirect:", flow)
            if flow["state"] != state:
                st.error("State mismatch: potential CSRF attack.")
                return
            try:
                result = app.acquire_token_by_auth_code_flow(flow, {'code': code}, scopes=settings.SCOPES)
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
            st.error("Flow not found in session.")
        return
    else:
        st.write("Successfully logged in motherfucker!!!")