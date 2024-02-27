from st_pages import Page, show_pages, add_page_title
import streamlit as st
import pandas as pd
import numpy as np
import time
from c_gruppen import Group
from db import DB
from c_schueler import Kid

st.set_page_config(layout="wide", page_title="Gruppen", page_icon=":man-woman-girl-girl:")
st.title(":man-woman-girl-girl:"+" Gruppen")

st.markdown("""
            Hier können Sie Gruppen/Stufen anlegen und bearbeiten. 
            Im Reiter 'Teilnehmer' können Sie die Kinder den entsprechenden Gruppen zuweisen. 
            Sie können ein Kind nur dann zu einer Gruppe hinzufügen, wenn es noch in keiner Gruppe ist.
            Um die Änderungen zu übernehmen drücken Sie bitte auf 'Speichern'.
            """)


# Initialize session state
if "showSession" not in st.session_state:
    st.session_state.showSession = 1


cl1, cl2, cl3 = st.columns([0.2,0.2,0.6])
button1_ph = cl1.button("Teilnehmer", on_click=lambda: st.session_state.__setitem__("showSession", 1), help="Klicken Sie hier um Kinder in Gruppen einzuteilen!")
button2_ph = cl2.button("Anlegen", on_click=lambda: st.session_state.__setitem__("showSession", 2), help="Klicken Sie hier um eine neue Gruppe anzulegen!")
button3_ph = cl3.button("Bearbeiten", on_click=lambda: st.session_state.__setitem__("showSession", 3), help="Klicken Sie hier um eine bestehende Gruppe zu bearbeiten!")

container = st.container()

# neue Gruppe anlegen
def button_gruppe_speichern_clicked():
    name = st.session_state.key_gruppen_name
    new_group = Group(name)

    if name == "":
        st.error("Bitte füllen Sie alle Felder aus!")
    elif new_group.check_if_group_exists():
        st.error(F"Die Gruppe '{name}' existiert bereits!")
    else:
        with st.spinner("Gruppe wird gespeichert..."):
            new_group.save_new_group()

        st.success(F"Die Gruppe '{name}' wurde erfolgreich gespeichert!")
        st.session_state.key_gruppen_name = ""
    
# Gruppe löschen wenn kein kind mehr in der Gruppe ist
def button_loeschen_clicked():
    name = st.session_state.key_ausg_Gruppe
    aus_group = Group(name)
    aus_group_ID = aus_group.get_groupID()
    db = DB()
    kids_in, _ = db.load_kids_in_group_or_available(aus_group_ID)
    db.__del__()

    if name == "":
        st.error("Bitte wählen Sie eine Gruppe aus!")
    elif kids_in != []:
        st.error(F"Die Gruppe '{name}' enthält noch Kinder und kann deshalb nicht gelöscht werden! Entfernen Sie zuerst die Kinder aus der Gruppe!")
    else:
        with st.spinner("Gruppe wird gelöscht..."):
            aus_group.delete()
        st.success(F"Die Gruppe '{name}' wurde erfolgreich gelöscht!")

# Kinder in Gruppen einfügen bzw entfernen
def button_speichern_clicked():
    gruppe = st.session_state.key_ausg_Gruppe
    ausg_gruppe_ID = Group(gruppe).get_groupID()
    kids_check = []
    kids_uncheck = []
    for kid in st.session_state:
        if kid.startswith("kid_i_") or kid.startswith("kid_n_"):
            if st.session_state[kid] == True:
                kids_check.append(kid)
            else:
                kids_uncheck.append(kid)

    if gruppe == "":
        st.error("Bitte wählen Sie eine Gruppe aus!")
    else:
        with st.spinner("Änderungen werden gespeichert..."):
            all_kids = kids_check + kids_uncheck
            for kid in all_kids:
                kid_name = kid.split("_")[2]
                firstnames = kid_name.split(" ")[0]
                lastnames = kid_name.split(" ")[1]

                if kid in kids_check:
                    kid_check = Kid(firstnames, lastnames, ausg_gruppe_ID)
                    kid_check.update_group(ausg_gruppe_ID)
                else:
                    kid_check = Kid(firstnames, lastnames, None)
                    kid_check.update_group(None)


        st.success(F"Die Änderungen wurden erfolgreich gespeichert!")

# Gruppe umbenennen
def button_speichern_clicked_bearbeiten():
    gruppe = st.session_state.key_ausg_Gruppe
    update_group = Group(gruppe)
    gruppe_neu = st.session_state.key_name_gruppe_neu
    new_group = Group(gruppe_neu)
    if gruppe == "":
        st.error("Bitte wählen Sie eine Gruppe aus!")
    elif gruppe_neu == "":
        st.error("Bitte füllen Sie alle Felder aus!")
    elif new_group.check_if_group_exists():
        st.error(F"Die Gruppe '{gruppe_neu}' existiert bereits!")
    else:
        with st.spinner("Änderungen werden gespeichert..."):
            update_group.update(gruppe_neu)
        st.success(F"Die Gruppe '{gruppe}' wurde in '{gruppe_neu}' geändert!")

def teilnehmer():
    db = DB()
    gruppen = db.load_groups()
    
    container.selectbox(label="Gruppe auswählen",key="key_ausg_Gruppe", index=0, options=gruppen, help="Bitte hier die Gruppe auswählen die Sie anzeigen wollen!")
    ausg_gruppe = Group(st.session_state.key_ausg_Gruppe)
    ausg_gruppe_ID = ausg_gruppe.get_groupID()

    kids_in, kinds_nowhere = db.load_kids_in_group_or_available(ausg_gruppe_ID)
    db.__del__()

    for kid_in in kids_in:
        container.checkbox(label=kid_in, key="kid_i_"+kid_in, value=True, help="Bitte hier die Schüler auswählen die Sie in die Gruppe einfügen wollen!")
    for kid_nowhere in kinds_nowhere:
        container.checkbox(label=kid_nowhere, key="kid_n_"+kid_nowhere, value=False, help="Bitte hier die Schüler auswählen die Sie in die Gruppe einfügen wollen!")

    container.button(label="Speichern", on_click=button_speichern_clicked, help="Klicken Sie hier um die Änderungen zu speichern!")


def anlegen():
    container.text_input(label="Gruppenname", key="key_gruppen_name", placeholder="Name der Gruppe", help="Bitte hier den Namen der Gruppen eingeben die Sie anlegen wollen!")
    container.button(label="Speichern", on_click=button_gruppe_speichern_clicked, help="Klicken Sie hier um das Kind zu speichern!")

def bearbeiten():
    db = DB()
    gruppen = db.load_groups()
    db.__del__()
    container.selectbox(label="Gruppe auswählen",key="key_ausg_Gruppe", index=0, options=gruppen, help="Bitte hier die Gruppe auswählen die Sie bearbeiten wollen!")
    container.text_input(label="Gruppenname", key="key_name_gruppe_neu",value=st.session_state.key_ausg_Gruppe, placeholder="Name der Gruppe", help="Bitte hier den neuen Namen der Gruppe eingeben!")
    
    container.button(label="Löschen", on_click=button_loeschen_clicked, help="Klicken Sie hier um die Gruppe zu löschen!")
    container.button(label="Speichern", on_click=button_speichern_clicked_bearbeiten, help="Klicken Sie hier um die Änderungen zu speichern!")


if st.session_state.showSession == 1:
    teilnehmer()
elif st.session_state.showSession == 2:
    anlegen()
else:
    bearbeiten()

