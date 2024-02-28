import streamlit as st
import st_pages as stp
from db import DB
from encode import hash
import logging
# Function to show the main content

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s %(message)s')

st.set_page_config(layout="wide", page_title="VSGrade", page_icon=":school:")

def main():
    st.markdown("""
        # Willkommen zu VSGrade :school: 

        ---
                
        Beginnen Sie mit der Navigation auf der linken Seite.
                
        ---
    	"""
    )

    st.header("Dokumentation")
    st.markdown("""
                Dort können Sie jederzeit die Dokumentation zu diesem Programm einsehen.
                #
                #
                #
                #
                """
                )
    st.markdown("powered by ObSt")
    

    pages = [
        stp.Page("doc.py", "Dokumentation", ":page_with_curl:"),
        stp.Page("buecher.py", "Bücher", ":books:"),
        stp.Page("schueler.py", "Schüler", ":student:"),
        stp.Page("gruppen.py", "Gruppen", ":man-woman-girl-girl:"),
        stp.Page("benotung.py", "Benotung", ":1234:"),
        stp.Page("einstellungen.py", "Einstellungen", ":gear:")
    ]
        
    stp.show_pages(pages)
    

def login_pressed(name:str, password:str, token:str):
    # Load the credentials from the database
    db = DB()
    db_usernames, db_passwords = db.get_credentials()

    hashed_password = hash(password)
    hashed_token = None

    if token == None: #login
        if name in db_usernames and hashed_password == db_passwords[db_usernames.index(name)]:        
            st.session_state.logged_in = True
            db.set_UserToken_inSession(name, hashed_token)
            db.__del__()
            logging.info(f"User {name} logged in.")     
        else:
            st.error("The credentials you entered are incorrect.")

    else:   #register
        hashed_token = hash(token)   
        if db.check_token(hashed_token):
            if name not in db_usernames:
                db.save_credentials(name, hashed_password)
                logging.info(f"User {name} registered.")
                st.session_state.logged_in = True
                db.set_UserToken_inSession(name, hashed_token)

                db.__del__()
            else:
                st.error("The username is already in use.")


def login():
    db = DB()

    if db.get_session_token() is None or db.get_session_token() == "":
        st.title("Register Page")

        name = st.text_input("Name")
        password = st.text_input("Password", type="password")
        token = st.text_input("Token")

        st.button("Programm aktivieren", on_click=lambda: login_pressed(name, password, token))

    else:
        st.title("Login Page")
        name = st.text_input("Name")
        password = st.text_input("Password", type="password")

        st.button("Login", on_click=lambda: login_pressed(name, password, None))

    db.__del__()
    
# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
else:
    main()
