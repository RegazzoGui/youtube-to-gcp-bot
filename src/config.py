import os
from dotenv import load_dotenv

load_dotenv()

# Variaveis de ambiente
GCP_BUCKET = os.getenv("GCP_BUCKET")
GCP_CREDENTIALS = os.getenv("CGP_CREDENTIALS")
DOWNLOAD_PATH = os.getenv("DOWNLOAD_PATH", "/tmp")
DATE_AFTER = os.getenv("DATE_AFTER")
COOKIE_FILE = os.getenv("COOKIE_FILE")


# ETL Excel to BigQuery
SHAREPOINT_SITE_URL = os.getenv("SHAREPOINT_SITE_URL")
SHAREPOINT_CLIENT_ID = os.getenv("SHAREPOINT_CLIENT_ID")
SHAREPOINT_CLIENT_SECRET = os.getenv("SHAREPOINT_CLIENT_SECRET")
SHAREPOINT_FILE_PATH = os.getenv("SHAREPOINT_FILE_PATH")# Ex: https://suaempresa.sharepoint.com/sites/SeuTime
SHAREPOINT_CLIENT_ID = os.getenv("SHAREPOINT_CLIENT_ID")  # Client ID do Azure AD
SHAREPOINT_CLIENT_SECRET = os.getenv("SHAREPOINT_CLIENT_SECRET")  # Client Secret do Azure AD
SHAREPOINT_FILE_PATH = os.getenv("SHAREPOINT_FILE_PATH")  # Caminho do arquivo no SharePoint

BIGQUERY_PROJECT = os.getenv("BIGQUERY_PROJECT")
BIGQUERY_DATASET = os.getenv("BIGQUERY_DATASET")
BIGQUERY_TABLE = os.getenv("BIGQUERY_TABLE")
# Caminho para o arquivo JSON da Service Account (para autenticação no BQ)
SERVICE_ACCOUNT_PATH_BQ = os.getenv("SERVICE_ACCOUNT_PATH_BQ")