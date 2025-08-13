from transformers import pipeline

pipe = pipeline("text2text-generation", model="google/flan-t5-small")

COMMAND_MAPPER = {
    "disc space": "dir C:\\",
    "list files in current directory": "dir",
    "create file": "type nul > {filename}",
    "delete file": "del {filename}",
    "move to": "cd %USERPROFILE%\\{dirname}",
    "list files in": "dir %USERPROFILE%\\{dirname}",
    "show all running processes": "dir C:\\Windows\\System32\\*.exe",
    "terminate running process": "C:\\Windows\\System32\\taskkill.exe /IM {processname} /F",
    "show system information": "ver",
    "move file": "move {filename} %USERPROFILE%\\{destdir}",
    "show processes": "dir C:\\Windows\\System32\\*.exe",
    "taskkill": "C:\\Windows\\System32\\taskkill.exe /IM {processname} /F"  # New mapping for direct taskkill
}

def convert_to_command(user_input):
    # Extract parameters from user_input
    filename = extract_filename(user_input)
    dirname = extract_dirname(user_input)
    processname = extract_processname(user_input)
    destdir = extract_destdir(user_input)

    # Normalize user input for matching
    user_input_lower = user_input.lower()

    for key, command in COMMAND_MAPPER.items():
        if key.lower() in user_input_lower:
            # Replace placeholders with extracted parameters
            formatted_command = command
            if "{filename}" in formatted_command:
                formatted_command = formatted_command.format(
                    filename=filename or "newfile.txt",
                    destdir=destdir or "Documents"
                )
            elif "{dirname}" in formatted_command:
                formatted_command = formatted_command.format(
                    dirname=dirname or "Documents"
                )
            elif "{processname}" in formatted_command:
                formatted_command = formatted_command.format(
                    processname=processname or "notepad.exe"
                )
            elif "{destdir}" in formatted_command:
                formatted_command = formatted_command.format(
                    destdir=destdir or "Documents"
                )
            return formatted_command

    # Fallback to NLP model for unrecognized commands
    prompt = f"Convert this to a Windows terminal command: {user_input}"
    try:
        result = pipe(prompt, max_length=50, do_sample=False)[0]['generated_text']
        # Normalize taskkill if returned by NLP model
        if result.lower().startswith("taskkill"):
            processname = extract_processname(user_input) or "notepad.exe"
            return f"C:\\Windows\\System32\\taskkill.exe /IM {processname} /F"
        return result.strip()
    except Exception as e:
        print("Error in NLP layer:", str(e))
        return "echo Failed to interpret command"

def extract_filename(user_input):
    words = user_input.split()
    for word in words:
        if word.endswith((".txt", ".doc", ".pdf")):
            return word
    return None

def extract_dirname(user_input):
    dirs = ["Desktop", "Documents", "Downloads"]
    for dir_name in dirs:
        if dir_name.lower() in user_input.lower():
            return dir_name
    return None

def extract_processname(user_input):
    words = user_input.split()
    for word in words:
        if word.endswith((".exe")) or word in ["notepad", "calc"]:
            return word + (".exe" if not word.endswith(".exe") else "")
    return None

def extract_destdir(user_input):
    dirs = ["Desktop", "Documents", "Downloads"]
    words = user_input.split()
    for i, word in enumerate(words):
        if word.lower() in ["to", "into"] and i + 1 < len(words):
            next_word = words[i + 1]
            if next_word in dirs:
                return next_word
    return None