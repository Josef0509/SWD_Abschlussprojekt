import subprocess
import os

def launch_app():
    try:
        # get the folder where this script is located
        destination_folder = os.path.dirname(os.path.realpath(__file__))

        # Specify the Python interpreter within the virtual environment
        python_executable = os.path.join(destination_folder, 'venv', 'Scripts', 'python.exe')

        # Now that the virtual environment is activated, you can run streamlit
        main_script = os.path.join(destination_folder, 'main.py')
        print("Launching the app...")
        subprocess.run([python_executable, '-m', 'streamlit', 'run', main_script])

        
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
            

if __name__ == "__main__":
    launch_app()
    input("Press Enter to exit...")
