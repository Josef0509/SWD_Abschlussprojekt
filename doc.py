from st_pages import Page, show_pages, add_page_title
import streamlit as st

st.set_page_config(layout="wide", page_title="Dokumentation", page_icon=":page_with_curl:")
st.title(":page_with_curl:"+" Dokumentation")


st.header("Haftungsausschluss")
st.markdown(
    """
    Die Notensoftware VSGrade befindet sich in der Version 1.0.0 und wurde von ObSt entwickelt. 
    Es handelt sich um eine Beta-Version und daher können noch Fehler auftreten. 
    ObSt übernimmt keine Haftung für Fehler, die durch die Verwendung der Software entstehen. 
    """
)

st.header("Allgmeines")
st.markdown(
    """
    ### Navigation
    Die Navigation erfolgt über die Leiste auf der linken Seite. 
    """
)
st.markdown("""
            ### Widgets
            Sie interagieren mit dem Programm über Widgets. Diese sind mit einem Namen und einer Hilfe versehen. 
            Die Hilfe wird angezeigt, wenn Sie mit der Maus über das ? Symbol fahren. 
            Nachfolgend sehen Sie ein beispielhaftes Widget.
            """)
st.text_input("Texteingabe", "", placeholder="Hier können Sie etwas hineinschreiben", help="Hier stehen Hilfestellungen bzw. Beschreibungen")


