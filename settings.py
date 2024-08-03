from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()

environment = os.getenv('ENVIRONMENT', 'dev').lower()

if environment == 'prod':
    CLIENT_ID = os.getenv('PROD_AZURE_CLIENT_ID')
    TENANT_ID = os.getenv('PROD_AZURE_TENANT_ID')
    CLIENT_SECRET = os.getenv('PROD_AZURE_CLIENT_SECRET')
else:
    CLIENT_ID = os.getenv('DEV_AZURE_CLIENT_ID')
    TENANT_ID = os.getenv('DEV_AZURE_TENANT_ID')
    CLIENT_SECRET = os.getenv('DEV_AZURE_CLIENT_SECRET')

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
# REDIRECT_PATH = "/getAToken" 
# SCOPES = ["https://graph.microsoft.com/.default"] 
SCOPES = ["User.Read"]

# Database

if environment == 'prod':
    DB_HOST = os.getenv('PROD_DB_HOST')
    DB_PORT = os.getenv('PROD_DB_PORT')
    DB_NAME = os.getenv('PROD_DB_NAME')
    DB_USER = os.getenv('PROD_DB_USER')
    #DB_PASSWORD = os.getenv('PROD_DB_PASSWORD')
else:
    DB_HOST = os.getenv('DEV_DB_HOST')
    DB_PORT = os.getenv('DEV_DB_PORT')
    DB_NAME = os.getenv('DEV_DB_NAME')
    DB_USER = os.getenv('DEV_DB_USER')
    #DB_PASSWORD = os.getenv('DEV_DB_PASSWORD')

if not all([CLIENT_ID, TENANT_ID, CLIENT_SECRET, DB_HOST, DB_PORT, DB_NAME, DB_USER]):
    raise ValueError("One or more environment variables have not been configured correctly.")

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        #password=DB_PASSWORD
    )