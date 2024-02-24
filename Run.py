import subprocess
import os

def get_input_directory():
    try:
        with open("config.txt", "r") as file:
            input_directory = file.readline().strip()
            return input_directory
    except FileNotFoundError:
        print("config.txt not found. Please run Installation.py first.")
        return None

def main():
    input_directory = get_input_directory()

    if input_directory:
        # Open PowerShell in interactive mode and run the commands
        process = subprocess.Popen(['powershell.exe', '-NoExit'])

        # Define commands to run in PowerShell
        commands = [
            f'cd {input_directory + "SWD_Abschlussprojekt/"}',
            './venv/Scripts/activate',
            f'streamlit run main.py'
        ]

        # Construct the PowerShell command string
        powershell_command = ';'.join(commands)

        # Run the commands in PowerShell
        process = subprocess.Popen(['powershell.exe', '-NoExit', '-Command', powershell_command])

        # Wait for the PowerShell process to finish
        process.wait()

if __name__ == "__main__":
    main()
