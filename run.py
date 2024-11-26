import subprocess
from flask import Flask, request, jsonify
import os as _o
import signal as _s

app = Flask(__name__)

# Keep track of active RTSP processes
active_processes = {}
# Processes
services_list = {
	"sentry_mode" : {
		"script" : "app/workers/person_detection_worker.py",
		"description" : "Runs an object detection script to send notifications when people are detected in a frame",
		"is_running" : False
	},
	"trip_wire": {
		"script" : "app/workers/line_cross.py",
		"description" : "Runs a script that triggers a notification if a person is detected to cross a boundary line",
		"is_running" : False
	},
	"say_hi" : {
		"script" : "app/workers/say_hi.py",
		"description" : "Runs a script to say hi as a test",
		"is_running" : False
	},


}

# Start an RTSP process
@app.route('/start_process', methods=['GET'])
def start_process():
	data = request.json
	command = data.get("command")
	script_name = None
	args = data.get("video_url")

	if not command in services_list:
		return jsonify({"error" : "Command does not exist"}),400

	script_name = services_list[command]["script"]

	try:
		process = subprocess.Popen(['python', script_name , args], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		services_list[command]["is_running"] = True
		services_list[command]["process_id"] = process.pid
		# services_list[command]["process"] = process
		return jsonify({"message": f"{process.pid}: Command {command} executed successfully"}), 200
	except Exception as e:
		return jsonify({"error": f"Failed to execute command {command}: {str(e)}"}), 500

# End an RTSP process
@app.route('/end_process', methods=['GET'])
def end_process():
	data = request.json
	# process_name = data.get("name")
	command = data.get("command")

	if command not in services_list:
		return jsonify({"error" : "Command not found"}),400

	if services_list[command]["is_running"]:
		try:
			_o.kill(services_list[command]["process_id"], _s.SIGTERM)
			del services_list[command]["process_id"]
			services_list[command]["is_running"] = False
			return jsonify({"message": f"Successfully terminated command {command}"}), 200
		except Exception as e:
			return jsonify({"error": f"Failed to terminate command {command}: {str(e)}"}), 500
	return jsonify({"error": "Command is not running"}),500

	# # if not process_name:
	# # 	return jsonify({"error": "Missing 'name' in request data"}), 400

	# # if process_name not in active_processes:
	# # 	return jsonify({"error": f"Process {process_name} is not running"}), 400

	# try:
	# 	process = active_processes[process_name]["process"]
	# 	process.terminate()
	# 	process.wait()
	# 	del active_processes[process_name]
	# 	return jsonify({"message": f"Process {process_name} terminated successfully"}), 200
	# except Exception as e:
	# 	return jsonify({"error": f"Failed to terminate process {process_name}: {str(e)}"}), 500

# Get status of all processes
@app.route('/status', methods=['GET'])
def status():
	list_copy = services_list.copy()
	for _ in list_copy.values():
		_.pop("process",None)
	return jsonify(list_copy)

@app.route('/notify', methods=['POST'])
def notify():
    data = request.json
    title = data.get("title", "Notification")  # Default title if none provided
    message = data.get("message")

    if not message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # Call the notification.py script with the title and message
        result = subprocess.run(
            ['python', 'app/utils/notification.py', title, message],  # Adjust the script path if necessary
            capture_output=True,
            text=True
        )

        # Check if the script ran successfully
        if result.returncode == 0:
            return jsonify({"message": "Notification sent successfully", "output": result.stdout}), 200
        else:
            return jsonify({"error": "Failed to send notification", "details": result.stderr}), 500

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000, debug=True)
