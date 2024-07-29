import streamlit as st
from msal import ConfidentialClientApplication
import settings
import authentication

# Aquí inicializa tu aplicación confidencial de MSAL
app = ConfidentialClientApplication(
    settings.CLIENT_ID,
    authority=settings.AUTHORITY,
    client_credential=settings.CLIENT_SECRET,
)

# Aquí obtienes el código de autorización desde la URL
query_params = st.experimental_get_query_params()
code = query_params.get('code', [None])[0]

if code:
    # Intercambia el código por un token de acceso
    result = app.acquire_token_by_authorization_code(
        code,
        scopes=settings.SCOPES,
        redirect_uri=f"{authentication.base_url}{settings.REDIRECT_PATH}"
    )
    if 'access_token' in result:
        st.success("Successfully logged in!")
        st.write(result['account']['username'])
    else:
        st.error("Failed to log in.")
        st.write(result.get('error_description', ''))
else:
    st.error("Authorization code not found in the request.")
