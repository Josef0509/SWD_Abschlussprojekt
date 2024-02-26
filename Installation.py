import subprocess
import os



def install():
    # Ask the user for the directory where to install
    install_directory = input("Enter the directory where you want to install: ")

    # Open PowerShell and navigate to the specified directory
    process = subprocess.Popen(['powershell.exe', '-NoExit'])

    desktop_pfad = os.path.join(os.path.expanduser("~"), "Desktop") #hier OneDrive weil mein Laptop kacke ist lol

    # Define commands to run in PowerShell
    commands = [
    'Set-ExecutionPolicy RemoteSigned',#setze Execution Policy auf RemoteSigned zur Ausführung von Skripten
    'cmd /c "curl -o python-installer.exe https://www.python.org/ftp/python/3.9.0/python-3.9.0.exe && python-installer.exe"', #installiere Python
    'winget install --id Git.Git -e --source winget', #installiere Git
    f'cd {install_directory}',
    'git clone https://github.com/Josef0509/SWD_Abschlussprojekt.git',
    'cd ./SWD_Abschlussprojekt',
    'python -m venv venv',
    './venv/Scripts/activate',
    'pip install streamlit st_pages matplotlib',
    f'New-Item -ItemType SymbolicLink -Path "{desktop_pfad}\ObSt.lnk" -Target {install_directory+"/SWD_Abschlussprojekt/Run.exe"}',
    f'echo {install_directory} > config.txt',  # Create config.txt with input_directory
    ]

    # Construct the PowerShell command string
    powershell_command = ';'.join(commands)

    # Open PowerShell in interactive mode and run the commands
    process = subprocess.Popen(['powershell.exe', '-NoExit', '-Command', powershell_command])

    #launch()

def launch():
    process = subprocess.Popen(['powershell.exe', '-NoExit'])

    # Define commands to run in PowerShell
    commands = [
        './venv/Scripts/activate',
        'streamlit run main.py'
    ]

    # Construct the PowerShell command string
    powershell_command = ';'.join(commands)

    # Open PowerShell in interactive mode and run the commands
    process = subprocess.Popen(['powershell.exe', '-NoExit', '-Command', powershell_command])

# Wait for the PowerShell process to finish
install()




#Need Python
#Need GitBash
#Need Execution Policy to be set to RemoteSigned
