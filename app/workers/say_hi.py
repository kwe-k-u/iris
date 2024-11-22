import requests
import time
import hashlib
from datetime import datetime, timedelta


# Define the Iris server URL
IRIS_URL = "http://localhost:5000/notify"
notification_queue = {}


def send_notification(message):
    def can_send():
        message_hash = hashlib.sha256(message.encode()).hexdigest()
        current_time = datetime.now()
        if message_hash in notification_queue:
            message_time = notification_queue[message_hash]

            if current_time - message_time < timedelta(minutes=5):
                return False
        notification_queue[message_hash] = current_time
        return True

    try:
        if not can_send():
            return
        # Data to be sent to the Iris endpoint
        payload = {"message": message}

        # Make a POST request to the Iris /notify endpoint
        response = requests.post(IRIS_URL, json=payload)

        # Check the response status
        if response.status_code == 200:
            print("Notification sent successfully.")
        else:
            print(f"Failed to send notification: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    while True:
        send_notification("Working notifications?")
        time.sleep(5)  # Sleep for 5 seconds before sending the next "Hello"
