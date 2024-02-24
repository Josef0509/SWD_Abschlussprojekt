import subprocess
import os

def install():
    # Ask the user for the directory where to install
    install_directory = input("Enter the directory where you want to install: ")

    # Open PowerShell and navigate to the specified directory
    process = subprocess.Popen(['powershell.exe', '-NoExit'])

    # Define commands to run in PowerShell
    commands = [
        f'cd {install_directory}',
        'git clone https://github.com/Josef0509/SWD_Abschlussprojekt.git',
        'cd ./SWD_Abschlussprojekt',
        'python -m venv venv',
        './venv/Scripts/activate',
        'pip install streamlit st_pages matplotlib',
        f'New-Item -ItemType SymbolicLink -Path "C:/Users/obwal/Desktop/example.lnk" -Target {install_directory+"/SWD_Abschlussprojekt/Installation.exe"}'
    ]

    # Construct the PowerShell command string
    powershell_command = ';'.join(commands)

    # Open PowerShell in interactive mode and run the commands
    process = subprocess.Popen(['powershell.exe', '-NoExit', '-Command', powershell_command])


def check_if_installed():
    # Get the directory of the current Python script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to main.py
    main_py_path = os.path.join(current_directory, "main.py")

    # Check if main.py exists
    if os.path.exists(main_py_path):
        return True
    else:
        return False
    
def launch():
    process = subprocess.Popen(['powershell.exe', '-NoExit'])

    # Define commands to run in PowerShell
    commands = [
        './venv/Scripts/activate',
        f'streamlit run main.py'
    ]

    # Construct the PowerShell command string
    powershell_command = ';'.join(commands)

    # Open PowerShell in interactive mode and run the commands
    process = subprocess.Popen(['powershell.exe', '-NoExit', '-Command', powershell_command])


# Wait for the PowerShell process to finish
if check_if_installed():
    launch()
else:
    install()

