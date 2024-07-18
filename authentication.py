import msal # azure library to manage the authentication
from azure.identity import DefaultAzureCredential # This gets the credentials to access Azure
from azure.keyvault.secrets import SecretClient # This gets secrets from vault
import settings

# Accessing key vault
credential = DefaultAzureCredential() # find the credentials
client = SecretClient(vault_url=settings.KV_URI, credential=credential) # creating a client to interact with Azure Key Vault

# handling authentication of the application with Azure AD
app = msal.ConfidentialClientApplication(
    settings.CLIENT_ID, authority=settings.AUTHORITY,
    client_credential=settings.CLIENT_SECRET 
)

# AUTHENTICATION FUNCTIONS
# redirects user to Azure AD sign-in page
def get_auth_url():
    auth_url = app.get_authorization_request_url(
        scopes=settings.SCOPES,
        redirect_uri=f"https://cost-simulation-app-vthhaczahnv7bajvcnwnmj.streamlit.app{settings.REDIRECT_PATH}"
    )
    return auth_url

# takes authorization code and exchanges it for an "access token"
def get_token_from_code(callback_url):
    result = app.acquire_token_by_authorization_code(
        code=callback_url.split("code=")[1],
        scopes=settings.SCOPES,
        redirect_uri=f"https://cost-simulation-app-vthhaczahnv7bajvcnwnmj.streamlit.app{settings.REDIRECT_PATH}"
    )
    return result

# get a new access token without the user having to log in again
def refresh_token(refresh_token):
    result = app.acquire_token_by_refresh_token(refresh_token, scopes=settings.SCOPES)
    return result

