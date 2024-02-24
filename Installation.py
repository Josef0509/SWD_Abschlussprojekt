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
destination = input("Enter the destination path: ").strip()  # No need for raw string

if clone_repository(repo_url, destination):
    print("Repository cloned successfully!")
else:
    print("Error cloning repository.")

# Creating a venv there
#print("Creating a virtual environment...")
#venv_path = os.path.join(destination, 'venv')
#subprocess.run([sys.executable, '-m', 'venv', venv_path], check=True)

# Activating the virtual environment
#venv_activate_script = os.path.join(venv_path, 'Scripts', 'activate.bat')
#activate_cmd = f'call "{venv_activate_script}" && pip install streamlit st_pages matplotlib'
#subprocess.run(activate_cmd, shell=True)

# Directly install the packages without venv
subprocess.run([sys.executable, '-m', 'pip', 'install', 'streamlit', 'st_pages', 'matplotlib'], check=True)


# Done
print("Done.")
input("Press Enter to exit.")
