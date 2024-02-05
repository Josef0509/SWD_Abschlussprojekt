import streamlit as st
import st_pages as stp
# Function to show the main content

def main():
    st.markdown(
        """
        Notensoftware Erklärung am Ende einfügen
        """
    )
    pages = [
        stp.Page("doc.py", "Dokumentation", "📚"),
        stp.Page("buecher.py", "Bücher", "📚"),
        stp.Page("schueler.py", "Schüler", "📚"),
        stp.Page("gruppen.py", "Gruppen", "📚"),
        stp.Page("benotung.py", "Benotung", "📚")
    ]

    stp.show_pages(pages)
    stp.add_page_title()

def login_pressed(name:str, password:str):
    actual_email = "e"
    actual_password = "p"

    if name == actual_email and password == actual_password:
        # If login successful, set the session variable to True
        st.session_state.logged_in = True   
    else:
        st.error("The name or password you entered is incorrect.")


def login():
    st.title("Login Page")
    # Insert a form
    name = st.text_input("Name")
    password = st.text_input("Password", type="password")
    submit = st.button("Login", on_click=lambda: login_pressed(name, password))
    

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
else:
    main()
