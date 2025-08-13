import subprocess
import os

def execute_command(command):
    try:
        # Handle directory changes separately to maintain context
        if command.startswith("cd "):
            target_dir = command[3:].strip()
            target_dir = os.path.expandvars(target_dir)
            if os.path.isdir(target_dir):
                os.chdir(target_dir)
                return f"Directory changed to {target_dir}"
            else:
                user_profile = os.path.expandvars("%USERPROFILE%")
                available_dirs = [d for d in ["Documents", "Downloads"] if os.path.isdir(os.path.join(user_profile, d))]
                suggestion = f"Suggested directories: {', '.join(available_dirs)}" if available_dirs else "No common directories found."
                return f"Error changing directory: Directory '{target_dir}' does not exist. {suggestion}"
        # Handle file creation
        elif command.startswith("type nul >"):
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return "File created successfully"
            else:
                return f"Error creating file: {result.stderr}"
        # Handle process termination
        elif "taskkill" in command.lower():
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return "Process terminated successfully"
            else:
                taskkill_path = "C:\\Windows\\System32\\taskkill.exe"
                if not os.path.exists(taskkill_path):
                    return f"Error terminating process: taskkill.exe is not available in this environment."
                return f"Error terminating process: {result.stderr}"
        # Handle file move
        elif "move" in command:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return "File moved successfully"
            else:
                return f"Error moving file: {result.stderr}"
        # Handle disk space (dir C:\)
        elif command == "dir C:\\":
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                for line in result.stdout.splitlines():
                    if "bytes free" in line.lower():
                        return f"Disk Space: {line.strip()}"
                return "Disk Space: Unable to parse free space"
            else:
                return f"Error retrieving disk space: {result.stderr}"
        # Handle process listing (dir C:\Windows\System32\*.exe)
        elif command == "dir C:\\Windows\\System32\\*.exe":
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return f"System Executables (proxy for processes):\n{result.stdout}"
            else:
                return f"Error listing system executables: {result.stderr}"
        # Handle directory listing (dir)
        elif command == "dir":
            # Use dir /B /ON for bare, sorted output
            result = subprocess.run("dir /B /ON", shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout
            else:
                return f"Error listing directory: {result.stderr}"
        # Handle other commands
        else:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout or "Command executed successfully"
            else:
                return f"Error executing command: {result.stderr}"
    except Exception as e:
        return f"Error executing command: {str(e)}"