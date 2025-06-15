from flask import Flask, request, jsonify
from command_router import handle_command
from utils.auth import verify_slack_signature
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route("/slack/command", methods=["POST"])
def slack_command():
    if not verify_slack_signature(request):
        return "Unauthorized", 403

    command = request.form.get("command")
    response = handle_command(command, request.form)
    return jsonify(response)

if __name__ == "__main__":
    app.run(port=5000)
