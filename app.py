from flask import Flask, request, render_template
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from nlp_layer import convert_to_command
from executor import execute_command
from logger import log_command
from validator import validate_command

app = Flask(__name__)

# Set the working directory to flask_app at startup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

def parse_dir_output(output):
    items = output.strip().split('\n')
    return [{'name': item, 'date': '', 'size': ''} for item in items if item]

@app.route("/", methods=["GET", "POST"])
def index():
    output = ""
    converted_command = ""
    log_content = ""
    dir_items = []
    if request.method == "POST":
        user_input = request.form.get("command")
        if user_input.lower() == "exit":
            return render_template("index.html", output="Application exited.", converted_command="", log_content=log_content, dir_items=[])
        
        log_command(user_input)
        
        converted_command = convert_to_command(user_input)
        if not validate_command(converted_command):
            output = "Warning: Command contains forbidden action"
        else:
            output = execute_command(converted_command)
            if converted_command == "dir":
                dir_items = parse_dir_output(output)
                output = ""
        
        # Reset working directory after each command
        os.chdir(BASE_DIR)
    
    try:
        with open(os.path.join(BASE_DIR, "command_log.txt"), "r") as log_file:
            log_content = log_file.read()
    except FileNotFoundError:
        log_content = "No command log found."
    
    return render_template("index.html", output=output, converted_command=converted_command, log_content=log_content, dir_items=dir_items)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)