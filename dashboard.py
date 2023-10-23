import streamlit as st
from streamlit_option_menu import option_menu
from ingestion import ingestion


def dashboard():
    selected = option_menu(
        menu_title= "",
        options = ["Import", "Cleaning", "Processing", "Visualization"],
        orientation="horizontal",
        styles= {
            "nav-link-selected": {"background-color":"#004AAD"}
        }
    )

    if selected == "Import":
        ingestion()
