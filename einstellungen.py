from st_pages import Page, show_pages, add_page_title
import streamlit as st
from db import DB
import shutil
from datetime import datetime
import os

st.set_page_config(layout="wide", page_title="Einstellungen", page_icon=":gear:")
st.title(":gear:"+" Einstellungen")

def speichern_clicked():
    db = DB()
    db.save_User_backup_location(username, st.session_state.key_backup_loc)
    db.__del__()
    st.success("Backup-Ort erfolgreich gespeichert!")

def save_backup(autobackup: bool = False):
    try:
        # Source file path
        source_file = "Notensoftware.db"

        # Get the current timestamp
        timestamp = datetime.now().strftime('%Y_%m_%d__%H_%M_%S')

        ending = "A" if autobackup else "M"

        filename = f"NotensoftwareBackup_{timestamp}_{ending}"+".db"

        # Destination directory path
        destination_directory = backup_loc+"/"+filename

        # Copy the file to the destination directory
        shutil.copy(source_file, destination_directory)

        # Keep only the latest 5 backups
        files_with_creation_times = []
        for file_name in os.listdir(backup_loc):
            file_path = os.path.join(backup_loc, file_name)
            if os.path.isfile(file_path) and file_name.endswith(".db") and file_name.startswith("NotensoftwareBackup"):     #make sure to only work with the db files and not with other files in the directory
                creation_time = os.path.getctime(file_path)
                files_with_creation_times.append((file_path, creation_time))
        
        # Sort the files based on their creation times in ascending order (oldest first)
        sorted_files = sorted(files_with_creation_times, key=lambda x: x[1])
        files = len(sorted_files)
        max_files = 10
        
        if files > max_files:
            # Take the first num_files files from the sorted list and remove them
            for file_path, _ in sorted_files[:files-max_files]:
                os.remove(file_path)
        
        return filename
    except Exception as e:
        st.error(f"Es ist ein Fehler aufgetreten: {e}")
        return None
    

def backup_clicked():
    created_file = save_backup(autobackup=False)
    if created_file is not None:
        st.success("Backup der Datenbank erfolgreich erstellt! Dateiname: '"+created_file+"'")

def load_db_clicked():
    if file is not None:
        #making a backup of the old db
        auto_created_backup = save_backup(autobackup=True)
        st.success("Automatisches Backup der Datenbank erfolgreich erstellt! Dateiname: "+auto_created_backup)
        
        loaded_file = file.name

        #overwrite the old db with the new db
        file.name = "Notensoftware.db"  #change the name of the file to the name of the current database
        path = ""

        try:
            file_path = os.path.join(path, file.name)
            with open(file_path, "wb") as f:
                f.write(file.getvalue())
                
            st.success(f"Datenbank '{loaded_file}' erfolgreich geladen!")

        except Exception as e:
            st.error(f"Es ist ein Fehler aufgetreten: {e}")

    else: 
        st.error("Bitte wählen Sie eine Datenbank aus!")
        return

db = DB()   
username = db.get_User_in_Session()
backup_loc = db.get_User_backup_location(username)
db.__del__()

st.header("Backups erstellen")
st.markdown(
    """
    Sie können manuell ein Backup erstellen, indem Sie auf den Button "Backup erstellen" klicken.
    Es werden immer nur die letzten 10 Backups behalten um Speicher zu sparen!
    """
)
st.text_input("Backup-Ort", value=backup_loc, key="key_backup_loc", help="Geben Sie hier den absoluten Pfad zum Speichern des Backups ein. (zb: **C:\ Users\obwal\Desktop**)")

st.button("Speichern", help="Speichert den Backup-Ort in der Datenbank.", on_click=speichern_clicked)

st.button("Backup erstellen", help="Erstellt ein Backup der Datenbank und speichert es an den eingestellten Ort.", on_click=backup_clicked)


st.header("Datenbank laden")
st.markdown(
    """
    Sie können die Datenbank laden, indem Sie auf den Button "Datenbank laden" klicken. Diese ersetzt die aktuelle Datenbank durch die ausgewählte Datenbank. Es wird ein Backup der aktuellen Datenbank erstellt, bevor die neue Datenbank geladen wird.
    """
)

file = st.file_uploader("Datenbank auswählen", type=["db"], help="Wählen Sie hier die Datenbank aus, die Sie laden möchten.")
st.button("Datenbank laden", help="Lädt die ausgewählte Datenbank und ersetzt die aktuelle Datenbank.", on_click=load_db_clicked)


