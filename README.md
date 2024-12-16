# Iris - Camera Monitoring & Notification System

**Iris** is a camera monitoring and notification system that integrates with RTSP streams, performs real-time detection, and sends notifications based on configured events. It allows seamless management of camera feeds, real-time alerts, and integration with custom systems via a simple HTTP interface.

---

## Features

- **RTSP Stream Management**: Capture and stream video from RTSP sources.
- **Background Processing**: Handle video feeds, perform detection, and trigger events.
- **Notifications**: Send notifications to connected devices or systems via HTTP requests.
- **Customizable Configuration**: Easily configure camera feeds, stream sources, and notification behavior.
- **Python Integration**: Control the system programmatically using Python scripts.

---

## Table of Contents

1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Running Iris](#running-iris)
4. [Using Iris API](#using-iris-api)
5. [Sending Notifications](#sending-notifications)
7. [License](#license)

---

## Installation

### Prerequisites

- Python 3.8+
- Install required dependencies:

```bash
pip install -r requirements.txt
```
This will install the following dependencies:
- Flask for the API.
- opencv-python for video feed handling.
- requests for sending HTTP notifications.
- python-dotenv for environment variable management

## Configuration
Configuration values can be set in the .env file located in the ```/config/```. This file should be protected by .gitignore to keep your environment variables private. The firebase json for Cloud Message should be kept in the same folder

Example .env file:
```env
FIREBASE_CLOUD_MESSAGING_DEVICE_ID=sample-device-id
FIREBASE_CERT_PATH=path/to/serviceAccountKey.json
NOTIFICATION_URL=http://localhost:5000/notify
```


## Running Iris

To start the Iris server and monitor video streams, simply run the following command:

```bash
python app/server.py
```
This will start a Flask application that handles video stream processing and notifications.
Using Iris API

Iris exposes the following API endpoints:
- /notify
```curl
curl -X POST http://localhost:5000/end_process -H "Content-Type: application/json" -d '{  "message":"<message>"}'
```
- /status
```curl
curl -X GET http://localhost:5000/status -H "Content-Type: application/json"
```
- /end_process
```curl
curl -X GET http://localhost:5000/end_process -H "Content-Type: application/json" -d '{  "command": "<command>",  "camera_name" : "<name>"}'
```
- /start_process
```curl
curl -X GET http://localhost:5000/end_process -H "Content-Type: application/json" -d '{  "command": "<command>",  "camera_name" : "<name>",
"debug" :"false"}'
```



#### /notification
Method: POST

Send a notification to a connected device. You can specify the message content via JSON.

Request Body:
```json
{
  "message": "Camera feed detected motion"
}
```

Response:

```json
{
  "message": "Notification received"
}
```

## Sending Notifications

You can trigger notifications by calling the /notify endpoint directly. Alternatively, you can integrate the notification logic into your Python scripts.

To send a notification from a Python script, simply run the following:


To run this script from the terminal, pass the title and message as arguments:

```bash
python notification.py "Camera Alert" "Motion detected at front door"
```
This will trigger a notification on the device(s) connected.


## Contributing

    Fork the repository.
    Create a new branch (git checkout -b feature-name).
    Commit your changes (git commit -am 'Add new feature').
    Push to the branch (git push origin feature-name).
    Create a new Pull Request.

## License

This project is licensed under the MIT License.


This is a fully formatted markdown file that you can use as the `README.md` for the Iris project. Feel free to edit any specifics or add more details as needed for your project.