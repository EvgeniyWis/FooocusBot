from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os
import pickle
from PIL import Image


# Функция для сохранения изображений в Google Drive
def save_images(images: list[Image.Image], folder_name: str):
    # Настройка аутентификации Google Drive API
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    creds = None
    
    # Загрузка сохраненных учетных данных
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # Если нет действительных учетных данных, запросить авторизацию
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Сохранение учетных данных для будущего использования
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Создание сервиса Google Drive
    service = build('drive', 'v3', credentials=creds)

    # Создание папки
    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    folder = service.files().create(body=folder_metadata, fields='id').execute()
    folder_id = folder.get('id')

    # Загрузка изображений
    for i, image_path in enumerate(images):
        file_metadata = {
            'name': f'{folder_name}_{i}',
            'parents': [folder_id]
        }
        media = MediaFileUpload(image_path, mimetype='image/jpeg')
        service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()