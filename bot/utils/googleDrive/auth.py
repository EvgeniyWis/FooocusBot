import json
import os
import pickle

from aiogoogle.auth.creds import ClientCreds

import bot.app.config.constants as constants

SCOPES = ["https://www.googleapis.com/auth/drive"]
CLIENT_SECRET_FILE = os.path.join(str(constants.BASE_DIR), "bot", "secrets", "googleDrive.json")
TOKEN_PICKLE = os.path.join(str(constants.BASE_DIR), "bot", "secrets", "token.pickle")

# Чтение client_id и client_secret из googleDrive.json
with open(CLIENT_SECRET_FILE) as f:
    client_info = json.load(f)["installed"]

client_creds = ClientCreds(
    client_id=client_info["client_id"],
    client_secret=client_info["client_secret"],
    scopes=SCOPES,
    redirect_uri=client_info["redirect_uris"][0],
)

user_creds = None
if os.path.exists(TOKEN_PICKLE):
    with open(TOKEN_PICKLE, "rb") as token:
        creds_obj = pickle.load(token)
        # Преобразуем объект в словарь
        user_creds = {
            "access_token": creds_obj.token,
            "refresh_token": creds_obj.refresh_token,
            "expires_at": creds_obj.expiry.isoformat(),
            "token_type": "Bearer",
            "id_token": getattr(creds_obj, "id_token", None),
            "scope": creds_obj.scopes,
            "client_id": creds_obj.client_id,
            "client_secret": creds_obj.client_secret,
        }