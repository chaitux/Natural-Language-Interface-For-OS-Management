from nlp_layer import convert_to_command
from executor import execute_command
from logger import log_command
from validator import validate_command

def main():
    while True:
        user_input = input("Enter command: ")
        if user_input.lower() == "exit":
            break

        log_command(user_input)

        command = convert_to_command(user_input)
        print(f"Converted command: {command}")

        if not validate_command(command):
            print("Warning: Command contains forbidden action")
            continue

        output = execute_command(command)
        print(f"Output: {output}")

if __name__ == "__main__":
    main()