import firebase_admin
from firebase_admin import credentials, messaging
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from config.config import FIREBASE_CLOUD_MESSAGING_DEVICE_ID, FIREBASE_CERT_PATH

# Initialize the Firebase Admin SDK
cred = credentials.Certificate(FIREBASE_CERT_PATH)  # Replace with your .json file path
firebase_admin.initialize_app(cred)

def send_fcm_notification(token, title, body):
    """
    Send a notification using Firebase Admin SDK.
    :param token: The FCM token of the target device.
    :param title: The notification title.
    :param body: The notification body.
    """
    try:
        # Create a message
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            topic="alerts"
            # token=token,  # Target device's FCM token
        )

        # Send the notification
        response = messaging.send(message)
        print(f"Notification sent successfully: {response}")
    except Exception as e:
        print(f"Error sending notification: {str(e)}")


# Example usage
if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("Usage: python notification.py \"title\" \"message\"")
		sys.exit(1)

	device_token = FIREBASE_CLOUD_MESSAGING_DEVICE_ID  # Replace with the FCM token of your app/device
	# Get the title and message from command-line arguments
	notification_title = sys.argv[1]
	notification_body = sys.argv[2]

	send_fcm_notification(device_token, notification_title, notification_body)
