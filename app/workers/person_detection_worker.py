import sys
import cv2
from ultralytics import YOLO
import os
import requests
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
	if len(sys.argv) != 2:
		send_notification("Usage: python video_processor_worker.py <video_url>")
		sys.exit(1)

	video_url = sys.argv[1]
	detect_classes = [0,1,2,3,5,7,16] #16: 'dog',7: 'truck',5: 'bus',0: 'person',1: 'bicycle',2: 'car',3: 'motorcycle'
	model = YOLO("yolo11m.pt")

	if not os.path.exists(video_url):
		send_notification("Couldn't find the vieo")
		sys.exit(1)


	send_notification(f"Processing video: {video_url}")

		# Open video file
	cap = cv2.VideoCapture(video_url)

	while cap.isOpened():
		ret, frame = cap.read()
		if not ret:
			send_notification(f"Failed to grab frame from {video_url}. Moving to the next video.")
			break

		# Run inference
		results = model.track(frame, conf=0.5,classes=detect_classes)

		if len(results[0].boxes) == 0:
			send_notification("no person detected")
		else:
			send_notification("Detected person")
		# Render results on the frame
		annotated_frame = results[0].plot()

		# Resize the frame to 700x700 max size
		annotated_frame = cv2.resize(annotated_frame, (700, 700))

		# Display the frame with annotated results
		cv2.imshow(f"YOLOv8 Detection - {video_url}", annotated_frame)

		# Wait for 'q' key press to close the window and continue to the next video
		key = cv2.waitKey(1) & 0xFF
		if key == ord('q'):
			cv2.destroyWindow(f"YOLOv8 Detection - {video_url}")
			break  # Exit the loop and move to the next video
		elif key == ord('c'):
			#break the file for loop
			should_break = True
			break

	cap.release()

	cv2.destroyAllWindows()
send_notification("Person detection terminated")