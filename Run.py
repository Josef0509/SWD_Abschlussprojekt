import subprocess
import os

def get_input_directory():
    try:
        with open("config.txt", "r") as file:
            input_directory = file.readline().strip()
            print(f"Input directory: {input_directory}")
            return input_directory
    except FileNotFoundError:
        print("config.txt not found. Please run Installation.py first.")
        return None

def launch():
    # Setze das Arbeitsverzeichnis auf das Verzeichnis des ursprünglichen Skripts
    print("Pfad zum Projektordner wird geladen...")
    input_directory = os.chdir(os.path.dirname(os.path.realpath(__file__)))
    print(f"Working directory: {input_directory}")


    #print("Pfad zum Projektordner wird geladen...")
    #input_directory = get_input_directory()

    if input_directory:
        # Konstruiere den vollen Pfad zum Unterordner
        print("Konstruiere den vollen Pfad zum Unterordner...")
        project_directory = os.path.join(input_directory, "SWD_Abschlussprojekt")

        # Überprüfe, ob der Projektordner existiert
        if not os.path.exists(project_directory):
            print(f"Project directory '{project_directory}' not found.")
            return

        

        # PowerShell-Befehle vorbereiten
        powershell_commands = [
            f'cd "{project_directory}"',
            '.\\venv\\Scripts\\Activate',
            'streamlit run main.py'
        ]

        # PowerShell-Befehle in einer Zeichenkette verbinden
        powershell_command = ';'.join(powershell_commands)

        # PowerShell-Prozess starten
        process = subprocess.Popen(['powershell.exe', '-NoExit', '-Command', powershell_command])

        # Warten, bis der PowerShell-Prozess beendet ist
        process.wait()

launch()
