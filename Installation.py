import subprocess
import sys
import os

def clone_repository(repo_url, destination):

    try:
        subprocess.run(['git', 'clone', repo_url, destination], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False
    
    return True

repo_url = "https://github.com/Josef0509/SWD_Abschlussprojekt.git"
destination = input(r"Enter the destination path:").strip()  # Using raw string

if clone_repository(repo_url, destination):
    print("Repository cloned successfully!")
else:
    print("Error cloning repository.")

# Creating a venv there
print("Creating a virtual environment...")
subprocess.run([sys.executable, '-m', 'venv', os.path.join(destination, 'venv')], check=True)

# Activating the virtual environment
venv_activate_script = os.path.join(destination, 'venv', 'Scripts', 'activate.bat')
activate_cmd = f'call "{venv_activate_script}" && pip install streamlit st_pages matplotlib'
subprocess.run(activate_cmd, shell=True)

# Done
print("Done.")
input("Press Enter to exit.")
