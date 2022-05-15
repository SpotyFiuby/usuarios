import os

import firebase_admin
from firebase_admin import auth, credentials  # pylint: disable=unused-import

# Fetch the service account key JSON file contents
cred = credentials.Certificate('credentials.json')

# Initialize the app with a custom auth variable, limiting the server's access
firebaseApp = firebase_admin.initialize_app(cred)

FIREBASE_WEB_API_KEY = os.environ.get("FIREBASE_WEB_API_KEY")
