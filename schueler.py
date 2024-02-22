from st_pages import Page, show_pages, add_page_title
import streamlit as st
import pandas as pd
import numpy as np
import time
from db import DB
from c_schueler import Kid
from c_buecher import Book
from c_benotung import gradeTOPercentage, percentageTOGrade

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


st.set_page_config(layout="wide", page_title="Schüler:innen", page_icon=":student:")
st.title(":student:"+" Schüler:innen")

# Initialize session state
if "showSession" not in st.session_state:
    st.session_state.showSession = 1

cl1, cl2, cl3 = st.columns([0.15,0.15,0.7])
button1_ph = cl1.button("Übersicht", on_click=lambda: st.session_state.__setitem__("showSession", 1), help="Klicken Sie hier um zur individuellen Schüleransicht zu gelangen!")
button2_ph = cl2.button("Anlegen", on_click=lambda: st.session_state.__setitem__("showSession", 2), help="Klicken Sie hier um ein neues Kind anzulegen!")
button3_ph = cl3.button("Bearbeiten", on_click=lambda: st.session_state.__setitem__("showSession", 3), help="Klicken Sie hier um ein bestehendes Kind zu bearbeiten!")

container = st.container()

def button_export_clicked():
    with st.spinner("Daten werden exportiert..."):
            # Daten wirklich exportieren
            pass
    st.success(F"Erfolgsmeldung")

def button_kind_speichern_clicked():
    vorname = st.session_state.key_vorname_schueler
    nachname = st.session_state.key_nachname_schueler
    if vorname == "" or nachname == "":
        st.error("Bitte füllen Sie alle Felder aus!")
    else:
        new_kid = Kid(vorname, nachname)
        if not new_kid.check_if_kid_name_exists():
            with st.spinner("Kind wird gespeichert..."):
                new_kid.save_new_kid()
            st.success(F"Das Kind '{vorname} {nachname}' wurde erfolgreich gespeichert!")
            st.session_state.key_vorname_schueler = ""
            st.session_state.key_nachname_schueler = ""
        else:
            st.error("Dieses Kind existiert bereits!")
    
def button_loeschen_clicked():
    name = st.session_state.key_ausg_Kind
    vorname = name.split(" ")[0]
    nachname = name.split(" ")[1]

    if name == None:
        st.error("Bitte wählen Sie ein Kind aus!")
    else:
        delete_kid = Kid(vorname, nachname)
        with st.spinner("Kind wird gelöscht..."):
            delete_kid.delete()
        st.success(F"Das Kind '{name}' wurde erfolgreich gelöscht!")

def button_speichern_clicked():
    name_alt = st.session_state.key_ausg_Kind
    if name_alt != None:
        vorname_alt = name_alt.split(" ")[0]
        nachname_alt = name_alt.split(" ")[1]

        vorname_neu = st.session_state.key_vorname_schueler_neu
        nachname_neu = st.session_state.key_nachname_schueler_neu

        if vorname_neu == "" or nachname_neu == "":
            st.error("Bitte füllen Sie alle Felder aus!")
        else: 
            update_kid = Kid(vorname_neu, nachname_neu)
            if not update_kid.check_if_kid_name_exists():
                with st.spinner("Kind wird gespeichert..."):
                    update_kid.update_name(vorname_alt, nachname_alt)
                st.success(F"Das Kind '{vorname_alt} {nachname_alt}' wurde in '{vorname_neu} {nachname_neu}' geändert!")
            else:
                st.error("Dieses Kind existiert bereits!")
    else:
        st.error("Bitte wählen Sie ein Kind aus!")


def uebersicht():
    db = DB()
    kids = db.load_kids()    
    container.selectbox(label="Kind auswählen",key="key_ausg_Kind", index=0, options=kids, help="Bitte hier das Kind auswählen das Sie anzeigen wollen!")
    books = db.load_books()
    db.__del__()

    c_books = []
    for book in books:
        c_books.append(Book(book))

    selected_kid = Kid(st.session_state.key_ausg_Kind.split(" ")[0], st.session_state.key_ausg_Kind.split(" ")[1])

    grade_data = {}

    # Iterate through each book
    for book in c_books:
        # Get grades for the current book
        grades = selected_kid.get_grades_with_bookID(book.get_ID())
        weights = selected_kid.get_weights_with_bookID(book.get_ID())

        grades_percentage = []
        for grade in grades:
            grades_percentage.append(gradeTOPercentage(grade))

        # Assign grades to the dictionary with the book name as the key
        grade_data[book.get_name()] = grades_percentage

        possible_points = sum(weights)
        achieved_points = sum([a*b/100 for a,b in zip(grades_percentage, weights)])
        try:
            percentage = achieved_points*100/possible_points
        except ZeroDivisionError:
            percentage = 0

        if grades != []:
            container.write(F"**Fach:** {book.get_name()}: **Note: {np.round(percentageTOGrade(percentage),3)}**  [{possible_points} / {achieved_points} Punkten erreicht = {np.round(percentage,2)}%]")
        else:
            container.write(F"**Fach:** {book.get_name()}: **Note: -**")      

    #fill the dictionary with the same length#
    max_len = max([len(grade_data[book]) for book in grade_data])
    for book in grade_data:
        while len(grade_data[book]) < max_len:
            grade_data[book].append(None)
    

    # Create DataFrame from the dictionary
    df = pd.DataFrame(grade_data)

    container.line_chart(df)

    # Create the line chart
    plt.figure(figsize=(10, 6))
    plt.plot(df)
    plt.xlabel('Index')
    plt.ylabel('Values')
    plt.title(f'Notenübersicht: {st.session_state.key_ausg_Kind.split(" ")[0]} {st.session_state.key_ausg_Kind.split(" ")[1]}')
    plt.legend(df.columns, loc='upper right')

    # Export the chart to PDF
    plt.savefig('Notenuebersicht.pdf')

    # Provide download button for the PDF
    container.download_button(
        label="Chart Exportieren",
        data=open('Notenuebersicht.pdf', 'rb').read(),
        file_name='Notenuebersicht.pdf',
        mime='application/pdf',
    )

def anlegen():
    container.text_input(label="Vorname", key="key_vorname_schueler", placeholder="Vorname des Kindes", help="Bitte hier den Vornamen des Kindes eingeben das Sie anlegen wollen!")
    container.text_input(label="Nachname", key="key_nachname_schueler", placeholder="Nachname des Kindes", help="Bitte hier den Nachnamen des Kindes eingeben das Sie anlegen wollen!")

    container.button(label="Speichern", on_click=button_kind_speichern_clicked, help="Klicken Sie hier um das Kind zu speichern!")

def bearbeiten():
    db = DB()
    kids = db.load_kids()
    db.__del__()
    container.selectbox(label="Kind auswählen",key="key_ausg_Kind", index=0, options=kids, help="Bitte hier das Kind auswählen das Sie anzeigen wollen!")
    
    if kids != []:
        vorname_alt = st.session_state.key_ausg_Kind.split(" ")[0]
        nachname_alt = st.session_state.key_ausg_Kind.split(" ")[1]
    else:
        vorname_alt = ""
        nachname_alt = ""
    
    container.text_input(label="Vorname", key="key_vorname_schueler_neu",value=vorname_alt, placeholder="Vorname des Kindes", help="Bitte hier den neuen Vornamen des Kindes eingeben!")
    container.text_input(label="Nachname", key="key_nachname_schueler_neu", value=nachname_alt, placeholder="Nachname des Kindes", help="Bitte hier den neuen Nachnamen des Kindes eingeben!")

    container.button(label="Löschen", on_click=button_loeschen_clicked, help="Klicken Sie hier um das Kind zu löschen!")
    container.button(label="Speichern", on_click=button_speichern_clicked, help="Klicken Sie hier um die Änderungen zu speichern!")


if st.session_state.showSession == 1:
    uebersicht()
elif st.session_state.showSession == 2:
    anlegen()
else:
    bearbeiten()

