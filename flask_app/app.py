from flask import Flask, request, render_template
import os
import sys

# Add parent directory to path to import existing modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from nlp_layer import convert_to_command
from executor import execute_command
from logger import log_command
from validator import validate_command

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    output = ""
    converted_command = ""
    log_content = ""
    if request.method == "POST":
        user_input = request.form.get("command")
        if user_input.lower() == "exit":
            return render_template("index.html", output="Application exited.", converted_command="", log_content=log_content)
        
        # Log the command
        log_command(user_input)
        
        # Convert and validate the command
        converted_command = convert_to_command(user_input)
        if not validate_command(converted_command):
            output = "Warning: Command contains forbidden action"
        else:
            # Execute the command
            output = execute_command(converted_command)
    
    # Read the command log
    try:
        with open(os.path.join(os.path.dirname(__file__), "command_log.txt"), "r") as log_file:
            log_content = log_file.read()
    except FileNotFoundError:
        log_content = "No command log found."
    
    return render_template("index.html", output=output, converted_command=converted_command, log_content=log_content)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)