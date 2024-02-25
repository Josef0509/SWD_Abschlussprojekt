import subprocess
import os



def launch():
    #hole den Pfad zum Projektordner des symlinks
    print("Pfad zum Projektordner wird geladen...")
    input_directory = "C:/Users/sandr/Desktop/TEST/SWD_Abschlussprojekt"

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