from st_pages import Page, show_pages, add_page_title
import streamlit as st
import pandas as pd
import numpy as np
from db import DB
from tkinter import filedialog

# Initialize session state
if "showSession" not in st.session_state:
    st.session_state.showSession = 1

add_page_title()
container = st.container()


cl1, cl2, cl3 = st.columns([0.15, 0.15, 0.7])



# ------------------------------------------------------------------------------------------------------------------------------
def uebersicht():
    st.header("Benotungsübersicht")
    db = DB()

    buecher = db.query("SELECT name FROM Book")  # returns tuples
    buecher = [buch[0] for buch in buecher] if buecher else []

    selected_book = container.selectbox(label="Buch auswählen", key="key_ausg_Buch", index=0, options=buecher,
                                        help="Bitte hier das Buch auswählen das Sie anzeigen wollen!")

    seitenanz_aus_DB = db.query("SELECT pages FROM Book WHERE name = ?", (selected_book,))
    seitenanz_aus_DB = seitenanz_aus_DB[0][0] if seitenanz_aus_DB and seitenanz_aus_DB[0] else None

    kids = db.query("SELECT firstname, lastname FROM Kid")  # returns tuples
    if kids != []:
        kids = [kid[0] + " " + kid[1] for kid in kids]  # convert to list

    if seitenanz_aus_DB:
        container.write(f"Seitenanzahl: {seitenanz_aus_DB}")

        # Fetch kid names and create a DataFrame with random data
        kids = db.query("SELECT firstname, lastname FROM Kid")
        if kids != []:
            kids = [f"{kid[0]} {kid[1]}" for kid in kids]
            df = pd.DataFrame(index=kids, columns=[f"S. {i}" for i in range(1, seitenanz_aus_DB + 1)])
            df.insert(0, 'Kid Name', kids)  # Insert Kid Names as the first column

            # Display editable data in Streamlit's data editor
            edited_data = st.data_editor(df)

            # Check if the data has been edited
            if edited_data is not None and st.button("Save Changes to Database"):
                # Update the database with the edited data
                update_database_with_edited_data(edited_data)

            # Open file explorer for the user to choose the file path
            file_path = "C:\\Users\\sandr\\OneDrive\\Desktop\\test\\export.csv"

            # Export the DataFrame to the specified file path
            if st.button("Export to CSV"):
                df.to_csv(file_path, sep='\t')
                st.success(f"Data successfully exported to {file_path}")

    else:
        container.write("Das Buch hat keine Seitenanzahl.")


def update_database_with_edited_data(edited_data):
    # Assuming DB class has a method for updating the data
    # Modify this according to your database structure and update methods
    db = DB()
    db.update_data(edited_data)
    st.success("Changes saved to the database!")







#------------------------------------------------------------------------------------------------------------------------------
if st.session_state.showSession == 1:
    uebersicht()
else:
    pass
