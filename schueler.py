from st_pages import Page, show_pages, add_page_title
import streamlit as st
import time


add_page_title()


def button_export_clicked():
    person = st.session_state.key_ausg_person
    if person == "":
        st.error("Bitte wählen Sie eine Person aus!")
    else:
        with st.spinner("Person wird exportiert..."):
            pass
        st.success(F"Die Person '{person}' wurde erfolgreich exportiert!")





tab_uebersicht, tab_bearbeiten = st.tabs(["Übersicht", "Bearbeiten"])

with tab_uebersicht:
    personen = ["Josef", "Giuseppe 2", "Josi"]    #tatstächlich aus der Datenbank holen

    st.selectbox(label="Person auswählen",key="key_ausg_person", index=0, options=personen, help="Bitte hier die Person auswählen die Sie anzeigen wollen!")
    

    st.button(label="Export", on_click=button_export_clicked, help="Klicken Sie hier um die Person zu exportieren!")
