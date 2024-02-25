import subprocess
import os



def launch():
    #hole den Pfad zum Projektordner des symlinks
    print("Pfad zum Projektordner wird geladen...")
#aus config.txt Pfad nehmen
    try:
        with open("config.txt", "r") as file:
            input_directory = file.readline().strip()
            #füge SWD_Abschlussprojekt an den Pfad an
            input_directory = os.path.join(input_directory, "SWD_Abschlussprojekt")
            print(f"Input directory: {input_directory}")
    except FileNotFoundError:
        print("config.txt not found. Please run Installation.py first.")
        return None

    print(f"Working directory: {input_directory}")
    

    if input_directory:
        
        # PowerShell-Befehle vorbereiten
        powershell_commands = [
            f'cd {input_directory}',
            '.\\venv\\Scripts\\activate',
            'streamlit run main.py'
        ]

        # PowerShell-Befehle in einer Zeichenkette verbinden
        powershell_command = ';'.join(powershell_commands)

        # PowerShell-Prozess starten
        process = subprocess.Popen(['powershell.exe', '-NoExit', '-Command', powershell_command])

        # Warten, bis der PowerShell-Prozess beendet ist
        process.wait()

launch()






'''

def install():
    # Ask the user for the directory where to install
    install_directory = input("Enter the directory where you want to install: ")

    # Open PowerShell and navigate to the specified directory
    process = subprocess.Popen(['powershell.exe', '-NoExit'])

    desktop_pfad = os.path.join(os.path.expanduser("~"), "Desktop") #hier OneDrive weil mein Laptop kacke ist lol

    # Define commands to run in PowerShell
    commands = [
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


def get_input_directory():
    try:
        with open("config.txt", "r") as file:
            input_directory = file.readline().strip()
            print(f"Input directory: {input_directory}")
            return input_directory
    except FileNotFoundError:
        print("config.txt not found. Please run Installation.py first.")
        return None

'''