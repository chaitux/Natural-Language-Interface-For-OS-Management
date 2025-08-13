def validate_command(command):
    forbidden_commands = ["format", "rmdir", "reboot", "sfc", "chkdsk", "del *.*"]  # Removed shutdown
    for forbidden in forbidden_commands:
        if forbidden in command.lower():
            return False
    # Additional safety for file deletion and process termination
    if "del" in command.lower():
        if not any(command.endswith(ext) for ext in [".txt", ".doc", ".pdf"]):
            return False
    if "taskkill" in command.lower():
        if not any(proc in command for proc in ["notepad.exe", "calc.exe"]):
            return False
    # Warn about shutdown but allow execution
    if "shutdown" in command.lower():
        print("Warning: Shutdown command detected. Proceeding with caution.")
        return True
    return True