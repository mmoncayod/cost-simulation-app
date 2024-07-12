from dotenv import load_dotenv
import os

# Load the enviiroment variables from .env
load_dotenv()

KEY_VAULT_NAME = os.getenv('KEY_VAULT_NAME')
KV_URI = f"https://{KEY_VAULT_NAME}.vault.azure.net"
CLIENT_ID = os.getenv('AZURE_CLIENT_ID')
TENANT_ID = os.getenv('AZURE_TENANT_ID')
CLIENT_SECRET = os.getenv('AZURE_CLIENT_SECRET')
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
REDIRECT_PATH = "/getAToken" # this was defined as Redirect URI in Azure
SCOPES = ["User.Read"]

if not all([KEY_VAULT_NAME, CLIENT_ID, TENANT_ID, CLIENT_SECRET]):
    raise ValueError("One or more enviroment variables have not been configurated correctly.")