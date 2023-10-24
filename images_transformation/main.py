import streamlit as st
from streamlit_option_menu import option_menu
from images import data
from fonctions import *

X,y=data()

selected = option_menu(
menu_title=None,
options=["Manuel", "Auto"],  
menu_icon="cast", 
default_index=0,  
orientation="horizontal",
styles={
    "container": {"padding": "10px","color": "black", "width":"210px" ,"background-color": "#fafafa"},
    "icon": {"color" : "black",  "font-size": "10px"},
    "nav-link": { 
        "font-size": "10px",
        "color": "black",
        "text-align": "center",
        "margin": "0px"
        },
    "nav-link-selected": {"background-color": "green","color": "#FFE4E1"},
            },
        )


X_transform=None
if selected == "Manuel":
    
    width=st.slider('Width', min_value=1, max_value=X.shape[1])
    height=st.slider('Height', min_value=1, max_value=X.shape[2])
    if X.shape[-1]>2:
        dim=st.selectbox("La profondeur de couleur", [1, 3])
    aug_img=st.checkbox("Voulez vous augmentez le nombre de vos images")
    nor_img=st.checkbox("Voulez vous normalisez vos images")
    col1, col2= st.columns(2)
    with col1:
        submit=st.button("Submit")
    if submit:
        X_transform=reshape_image(X,height,width,dim)
        if dim==1:
            X_transform=X_transform[:,:,:,np.newaxis]
        if nor_img:
            X_transform=X_transform/255.0
        if aug_img:
            X_transform=data_aug(X_transform)
        col1,col2,col3 = st.columns([2,3,1])
        with col2:
            st.text("Voila un échantillon de votre data")   
        n_imgs(X_transform,n=2)

if selected == "Auto":
    st.markdown(f'<div style="text-align:center"><p>La méthode "Auto" de traitement d\'images est une façon simple et automatisée d\'améliorer vos photos et images sans nécessiter de compétences avancées en data science. Avec cette méthode, vous pouvez rapidement corriger les problèmes courants des images.</p></div>', unsafe_allow_html=True)

    col1,col2,col3 = st.columns([3,1,3])
    with col2:
        submit=st.button("Submit")
    if submit:
        X_transform,X_reverse=pca_transform(X)
        col1,col2,col3 = st.columns([2,3,1])
        with col2:
            st.text("Voila un échantillon de votre data")                       
        n_imgs(X_reverse,n=2)