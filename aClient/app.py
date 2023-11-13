from flask import Flask, render_template, request, jsonify, send_file
import os
import paramiko
from scp import SCPClient
import time
from datetime import datetime

app = Flask(__name__)

# Load environment variables
SERVER_HOST = os.getenv("SERVER_HOST_ENV")
SERVER_USERNAME = os.getenv("SERVER_USERNAME_ENV")
SERVER_PATH_UP = os.getenv("SERVER_PATH_ENV_UP")
SERVER_PATH_DOWN = os.getenv("SERVER_PATH_ENV_DOWN")
SSH_PRIVATE_KEY_PATH = os.getenv("SSH_PRIVATE_KEY_PATH")


def create_ssh_client():
    """Create and return an SSH client, connected to the remote server."""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
        hostname=SERVER_HOST,
        username=SERVER_USERNAME,
        pkey=paramiko.Ed25519Key(filename=SSH_PRIVATE_KEY_PATH),
    )
    return ssh


def send_file_to_server(file_content, recordedfilename):
    """Send the file to the server using SCP."""
    ssh = create_ssh_client()
    destination = os.path.join(SERVER_PATH_UP, recordedfilename).replace("\\", "/")
    with SCPClient(ssh.get_transport()) as scp:
        scp.putfo(file_content, destination)
    ssh.close()


def get_latest_response_filename(timeout=240):
    """Retrieve the latest response filename from the server."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        ssh = create_ssh_client()
        stdin, stdout, stderr = ssh.exec_command(
            f"ls -t {SERVER_PATH_DOWN}/*.wav | head -n 1"
        )
        latest_filename = stdout.readline().strip()
        ssh.close()

        if latest_filename:
            return latest_filename
        time.sleep(5)  # wait for 5 seconds before retrying
    return None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process_audio", methods=["POST"])
def process_audio():
    if "audio_data" not in request.files:
        return jsonify({"error": "No audio file received"})

    audio_file = request.files["audio_data"]
    audio_filename = "received_audio.wav"
    audio_file.save(audio_filename)

    # Send audio file to the Oslomet server
    with open(audio_filename, "rb") as f:
        send_file_to_server(f, audio_filename)
        time.sleep(10)

    # Get the latest response file from the Oslomet server
    response_filename = get_latest_response_filename()
    if response_filename:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        unique_filename = f"downloaded_response_{timestamp}.wav"
        local_response_path = os.path.join(app.static_folder, unique_filename)
        ssh = create_ssh_client()
        with SCPClient(ssh.get_transport()) as scp:
            scp.get(response_filename, local_response_path)
        ssh.close()
        return jsonify({"response_file_path": f"/static/{unique_filename}"})
        # return send_file(local_response_path, as_attachment=True, mimetype="audio/wav")

    return jsonify({"status": "error", "message": "Response not received"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
