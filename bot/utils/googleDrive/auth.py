import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

# Авторизация и инициализация клиента google drive через OAuth 2.0
SCOPES = ["https://www.googleapis.com/auth/drive"]
current_dir = os.path.dirname(os.path.abspath(__file__))
CLIENT_SECRET_FILE = os.path.join(current_dir, "..", "..", "config", "googleDrive.json")
TOKEN_PICKLE = os.path.join(current_dir, "..", "..", "config", "token.pickle")

creds = None
# Проверяем, есть ли уже сохранённый токен
if os.path.exists(TOKEN_PICKLE):
    with open(TOKEN_PICKLE, 'rb') as token:
        creds = pickle.load(token)
# Если нет токена или он недействителен — проходим авторизацию
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
    # Сохраняем токен для будущих запусков
    with open(TOKEN_PICKLE, 'wb') as token:
        pickle.dump(creds, token)

service = build("drive", "v3", credentials=creds)
