import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

# 1. ඔබගේ JSON Key File එකෙහි නිවැරදි නම මෙතැනට ලබා දෙන්න
SERVICE_ACCOUNT_FILE = 'asymmetric-ray-506900-b6-793f5f9a7afc.json' 

# 2. ඔබගේ App එකෙහි නිවැරදි Package Name එක මෙතැනට ලබා දෙන්න
PACKAGE_NAME = 'com.brillionflash.app'

SCOPES = ['https://www.googleapis.com/auth/androidpublisher']

def create_play_service(api_json_path):
    if not os.path.exists(api_json_path):
        raise FileNotFoundError(f"JSON File එක හමු නොවීය: '{api_json_path}'. කරුණාකර JSON file එක script එක ඇති folder එකට Paste කරන්න.")

    credentials = service_account.Credentials.from_service_account_file(
        api_json_path, 
        scopes=SCOPES
    )
    return build('androidpublisher', 'v3', credentials=credentials)

try:
    print("Google Play Service Client එක සකස් වෙමින් පවතී...")
    play_service = create_play_service(SERVICE_ACCOUNT_FILE)
    print("Google Play Service Client එක සාර්ථකව සාදන ලදී!")

    print(f"App Package: {PACKAGE_NAME} සඳහා Edit Session එකක් ආරම්භ කරයි...")
    edit_request = play_service.edits().insert(packageName=PACKAGE_NAME, body={})
    edit_result = edit_request.execute()
    edit_id = edit_result['id']

    print(f"සාර්ථකයි! Edit Session ID එක: {edit_id}")

except Exception as e:
    print(f"\nදෝෂයක් සිදු විය: {e}")