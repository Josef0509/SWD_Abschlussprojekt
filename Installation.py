import subprocess
import os

def install():
    # Ask the user for the directory where to install
    install_directory = input("Enter the directory where you want to install: ")

    # Construct the full path to the installation directory
    install_path = os.path.join(install_directory, 'SWD_Abschlussprojekt')

    # Create the installation directory if it does not exist
    os.makedirs(install_path, exist_ok=True)

    # Clone the Git repository
    subprocess.run(['git', 'clone', 'https://github.com/Josef0509/SWD_Abschlussprojekt.git'], cwd=install_path, check=True)

    # Navigate to the project directory
    os.chdir(install_path)

    # Create a virtual environment and activate it
    subprocess.run(['python', '-m', 'venv', 'venv'], check=True)
    activate_script = os.path.join('venv', 'Scripts', 'activate')
    subprocess.run(['powershell.exe', '-NoProfile', '-Command', f'. {activate_script}'], check=True)

    # Install required packages
    subprocess.run(['pip', 'install', 'streamlit', 'st_pages', 'matplotlib', 'winshell'], check=True)

    # Create a symbolic link
    subprocess.run(['powershell.exe', '-Command', f'New-Item -ItemType SymbolicLink -Path "C:\Users\sandr\OneDrive\Desktop\example.lnk" -Target {os.path.join(install_path, "db.py")}'], check=True)


def check_if_installed():
    # Check if main.py exists in the current working directory
    return os.path.exists('main.py')


def launch():
    # Activate the virtual environment and run the Streamlit app
    activate_script = os.path.join('venv', 'Scripts', 'activate')
    subprocess.run(['powershell.exe', '-Command', f'New-Item -ItemType SymbolicLink -Path "C:\\Users\\sandr\\OneDrive\\Desktop\\example.lnk" -Target {os.path.join(install_path, "db.py")}'], check=True)


# Wait for the PowerShell process to finish
if check_if_installed():
    launch()
else:
    install()
