import os

import firebase_admin
from dotenv import load_dotenv
from firebase_admin import auth, credentials  # pylint: disable=unused-import

# upload environment variables
load_dotenv(".env")

# Fetch the service account key JSON file contents
cred = credentials.Certificate('credentials.json')

# Initialize the app with a custom auth variable, limiting the server's access
firebaseApp = firebase_admin.initialize_app(cred)

FIREBASE_WEB_API_KEY = os.environ.get("FIREBASE_WEB_API_KEY")
