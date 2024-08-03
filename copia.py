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

    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(settings.SCOPES, account=accounts[0]) 
    # Si no hay token en la session se inicia el flujo de autenticacion
    # flow: Contiene información necesaria para completar el flujo de autenticación (state, redirect_uri, scope, auth_uri, code_verifier, nonce, claims_challenge)
    
    if not result:
        # initiate_auth_code_flow inicia un nuevo flujo de autorización utilizando el protocolo de OAuth 2.0. 
        # El flow debe contener toda la información necesaria para que la aplicación pueda intercambiar el código de autorización por tokens de acceso y actualización.
        flow = app.initiate_auth_code_flow(settings.SCOPES, redirect_uri=redirect_uri)
        st.session_state["flow"] = flow
        st.session_state["auth_uri"] = flow["auth_uri"]
        st.session_state["state"] = flow["state"] 
        st.write("Flow initialized and stored in session:", flow) 

    # Insert flow in data base
        try:
            connection = settings.get_db_connection()
            cursor = connection.cursor()
            insert_query = """
            INSERT INTO auth_sessions (state, redirect_uri, scope, auth_uri, code_verifier, nonce, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, NOW())
            """
            cursor.execute(insert_query, (
                flow["state"],
                flow["redirect_uri"],
                ",".join(flow["scope"]),
                flow["auth_uri"],
                flow["code_verifier"],
                flow["nonce"]
            ))
            connection.commit()
            cursor.close()
            connection.close()
            st.write("Flow data stored in database")
        except Exception as e:
            st.write("Error storing flow data in database:", str(e))

    if result:
        st.write("Successfully logged in!")
        st.write(result['account']['username'])
    else:
        st.write("Please log in to see your username.")
#--- // ---#

def handle_redirect():
    # get authorization code from URL
    query_params = st.query_params
    code = query_params.get("code", [None])[0] # this is ok -- code is the authorization code sent by Azure AD after user authentication.
    st.write("Query Params:", query_params) 

    if code:
        st.write("Query Params 2:", query_params) 
        st.write("Session State:", st.session_state)

        # Recuperar el flow de la base de datos
        try:
            connection = settings.get_db_connection()
            cursor = connection.cursor()
            select_query = """
            SELECT state, redirect_uri, scope, auth_uri, code_verifier, nonce 
            FROM auth_sessions 
            WHERE state = %s
            """
            cursor.execute(select_query, (st.session_state["state"],))
            row = cursor.fetchone()
            cursor.close()
            connection.close()

            if row:
                flow = {
                    "state": row[0],
                    "redirect_uri": row[1],
                    "scope": row[2].split(","),
                    "auth_uri": row[3],
                    "code_verifier": row[4],
                    "nonce": row[5]
                }

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
                st.error("No matching flow found in database.")
        except Exception as e:
            st.error("An error occurred while retrieving flow data from database.")
            st.write(str(e))
    else:
        st.error("Authorization code not found in the request.")

