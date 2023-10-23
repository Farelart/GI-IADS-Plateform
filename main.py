import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
from dashboard import dashboard

st.set_page_config(layout="wide")

with st.sidebar:
    selected = option_menu(
        menu_title = "GI-IADS Plateform",
        options = ["Home","Dashboard","Statistics"],
        styles= {
            "nav-link-selected": {"background-color":"#004AAD"}
        }
    )

if selected == "Home":
    st.title("Bienvenue sur la plateforme GI-IADS")
    image = Image.open('pipeline.jpg')
    st.image(image, caption='', width=1200)
if selected == "Dashboard":
    dashboard()
if selected == "Statistics":
    pass