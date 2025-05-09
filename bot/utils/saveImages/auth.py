from google.oauth2 import service_account
from googleapiclient.discovery import build
import os


# Авторизация и инициализация клиента google drive
SCOPES = ['https://www.googleapis.com/auth/drive']
current_dir = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(current_dir, "..", "..", "config", "googleDrive.json")
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)