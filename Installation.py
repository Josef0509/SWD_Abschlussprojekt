import os
import subprocess
import sys

def main():
    config_file = 'config.txt'

    if not os.path.isfile(config_file):
        create_config_file(config_file)

    with open(config_file, 'r') as f:
        path = f.readline().strip()

    clone_repo(path)
    setup_venv(path)
    install_packages(path)
    run_streamlit(path)

def create_config_file(config_file):
    path = input("Geben Sie den Pfad zum Speichern der Dateien ein: ")
    with open(config_file, 'w') as f:
        f.write(path)

def clone_repo(path):
    subprocess.run(['git', 'clone', 'https://github.com/Josef0509/SWD_Abschlussprojekt', path])

def setup_venv(path):
    venv_path = os.path.join(path, '.venv')
    subprocess.run(['python', '-m', 'venv', venv_path])

    if sys.platform == 'win32':
        activate_venv_script = os.path.join(venv_path, 'Scripts', 'activate')
        subprocess.run([activate_venv_script], shell=True)
    else:
        activate_venv_script = os.path.join(venv_path, 'bin', 'activate')
        subprocess.run(['source', activate_venv_script], shell=True)


def install_packages(path):
    subprocess.run(['pip', 'install', 'streamlit', 'st_pages', 'matplotlib'])

def run_streamlit(path):
    subprocess.run(['streamlit', 'run', os.path.join(path, 'main.py')])

if __name__ == "__main__":
    main()
