import streamlit as st
from streamlit_option_menu import option_menu
from pages import page1, page2, page3
import authentication
import time
import settings
import msal


def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    st.write("# Welcome to Streamlit! 👋")

    st.sidebar.success("Select a demo above.")

    st.markdown(
        """
        Streamlit is an open-source app framework built specifically for
        Machine Learning and Data Science projects.
        **👈 Select a demo from the sidebar** to see some examples
        of what Streamlit can do!
        ### Want to learn more?
        - Check out [streamlit.io](https://streamlit.io)
        - Jump into our [documentation](https://docs.streamlit.io)
        - Ask a question in our [community
          forums](https://discuss.streamlit.io)
        ### See more complex demos
        - Use a neural net to [analyze the Udacity Self-driving Car Image
          Dataset](https://github.com/streamlit/demo-self-driving)
        - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
        """
    )

if __name__ == "__main__":
    run()

# Inicializar variables de sesión
if "auth_token" not in st.session_state:
    st.session_state.auth_token = None

# Manejar la redirección de Azure AD con el código de autorización
query_params = st.experimental_get_query_params()
if "code" in query_params:
    callback_url = query_params["code"][0]
    token_response = authentication.get_token_from_code(callback_url)
    if "access_token" in token_response:
        st.session_state.auth_token = token_response["access_token"]
        st.session_state.id_token_claims = token_response["id_token_claims"]
        st.experimental_rerun()
    else:
        st.error("Error de autenticación.")

# Si el usuario no ha iniciado sesión, mostrar el enlace para iniciar sesión
if st.session_state.auth_token is None:
    st.write("Por favor, inicia sesión con Azure AD.")
    auth_url = authentication.get_auth_url()
    st.write(f"[Iniciar sesión con Azure AD]({auth_url})")
else:
    st.write("Ya has iniciado sesión.")
    st.write("Access token:", st.session_state.auth_token)

    # Verificar si el usuario tiene el rol adecuado (si es necesario)
    roles = st.session_state.id_token_claims.get('roles', [])
    if "TuRolEsperado" in roles:
        st.write("Tienes acceso a la aplicación.")
    else:
        st.write("No tienes acceso a esta aplicación.")