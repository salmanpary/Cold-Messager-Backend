import os,json
from dotenv import load_dotenv

load_dotenv()

def generate_response(status_code, message):
    return {
        'statusCode': status_code,
        'body': json.dumps({"message": message})
    }

def load_env():
    return {
        "type": "service_account",
        "project_id": os.environ.get('FIREBASE_PROJECT_ID'),
        "private_key_id": os.environ.get('PRIVATE_KEY_ID'),
        "private_key": os.environ.get('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
        "client_email": os.environ.get('FIREBASE_CLIENT_EMAIL'),
        "client_id": os.environ.get('CLIENT_ID'),
        "auth_uri": os.environ.get('AUTH_URI'),
        "token_uri": os.environ.get('TOKEN_URI'),
        "auth_provider_x509_cert_url": os.environ.get('AUTH_PROVIDER_X509_CERT_URL'),
        "client_x509_cert_url": os.environ.get('CLIENT_X509_CERT_URL'),
        "universe_domain": "googleapis.com"
    }