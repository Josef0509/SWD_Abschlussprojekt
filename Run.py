import subprocess
import os


def launch():
    process = subprocess.Popen(['powershell.exe', '-NoExit'])

    # Define commands to run in PowerShell
    commands = [
        f'cd C:/Users/obwal/Desktop/TEST/SWD_Abschlussprojekt/',
        './venv/Scripts/activate',
        f'streamlit run main.py'
    ]

    # Construct the PowerShell command string
    powershell_command = ';'.join(commands)

    # Open PowerShell in interactive mode and run the commands
    process = subprocess.Popen(['powershell.exe', '-NoExit', '-Command', powershell_command])


# Wait for the PowerShell process to finish
launch()

