import os
from dotenv import load_dotenv

load_dotenv()

# Variaveis de ambiente
GCP_BUCKET = os.getenv("GCP_BUCKET")
GCP_CREDENTIALS = os.getenv("GCP_CREDENTIALS")
DOWNLOAD_PATH = os.getenv("DOWNLOAD_PATH", "/tmp")