import subprocess
import os
import sys



def launch():
    #hole den Pfad zum Projektordner des symlinks
    print("Pfad zum Projektordner wird geladen...")
    input_directory = "C:/Users/sandr/Desktop/TEST/SWD_Abschlussprojekt"

    print(f"Working directory: {input_directory}")

    


    if getattr(sys, 'frozen', False):
        # Das Skript wird als eigenständige ausführbare Datei ausgeführt (z. B. durch PyInstaller)
        exe_path = sys.executable
        original_working_directory = os.path.dirname(exe_path)
        print(f"Original Working Directory: {original_working_directory}")
        
    else:
        # Das Skript wird direkt interpretiert
        direct_intrepretation = os.getcwd()
        print(f"Direct Interpretation: {direct_intrepretation}")

    current_working_directory = os.getcwd()
    print(f"Current Working Directory: {current_working_directory}")
    

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