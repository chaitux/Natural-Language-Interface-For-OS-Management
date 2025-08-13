from datetime import datetime

def log_command(command):
    try:
        with open("command_log.txt", "a") as log_file:
            log_file.write(f"{datetime.now()} - {command}\n")
    except Exception as e:
        print(f"Error logging command: {str(e)}")