import subprocess
import os


def launch():

    current_dir = os.path.dirname(os.path.abspath(__file__))
    process = subprocess.Popen(['powershell.exe', '-NoExit'])

    # Define commands to run in PowerShell
    commands = [
        f'cd {current_dir}',
        './venv/Scripts/activate.bat',
        f'streamlit run main.py'
    ]

    # Construct the PowerShell command string
    powershell_command = ';'.join(commands)

    # Open PowerShell in interactive mode and run the commands
    process = subprocess.Popen(['powershell.exe', '-NoExit', '-Command', powershell_command])


# Wait for the PowerShell process to finish
launch()

