# /config/config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the environment variables
FIREBASE_CLOUD_MESSAGING_DEVICE_ID = os.getenv("FIREBASE_CLOUD_MESSAGING_DEVICE_ID")
FIREBASE_CERT_PATH=os.getenv("FIREBASE_CERT_PATH")
NOTIFICATION_URL=os.getenv("NOTIFICATION_URL")