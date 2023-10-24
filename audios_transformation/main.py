import streamlit as st
from streamlit_option_menu import option_menu
import os
import numpy as np
import matplotlib.pyplot as plt
from fonctions import  *

plt.style.use('classic')

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
def normalize(data):
    min_val = np.min(data)
    max_val = np.max(data)
    normalized_data = (data - min_val) / (max_val - min_val)
    return normalized_data
if selected == "Manuel":
    option=st.radio("Quelle forme voulez vous transformez votre audio",["Signal","Spectrogramme"])
    if option=="Spectrogramme":
        frame_length=st.slider('frame lenght', min_value=1, max_value=500)
        frame_step=st.slider('frame step', min_value=1, max_value=500)
        fft_length=st.slider('frequence lenght', min_value=1, max_value=500)
    submit=st.button("Submit")
    if submit:
        if option=="Signal":
            for fichier_audio in os.listdir(wavs_path):
                signal=extract_audio_signal(fichier_audio)
                fig, ax = plt.subplots()
                ax.plot(signal)
                ax.set_title('Voila a quoi ressemble votre data')
                st.pyplot(fig)
                break
            wav_files = ["file1", "file2", "file3"] 
            dataset = tf.data.Dataset.from_tensor_slices(wav_files)
            dataset = dataset.map(extract_audio_signal)
        if option=="Spectrogramme":
            col1,col2,col3 = st.columns([2,3,1])
            with col2:
                st.text("Voila a quoi ressemble votre data") 
            for fichier_audio in os.listdir(wavs_path):
                spectrogramme=encode_single_sample(fichier_audio,frame_length,frame_step,fft_length)
                spectrogramme=spectrogramme.numpy().T
                spectrogramme = (spectrogramme- np.min(spectrogramme)) / (np.max(spectrogramme) - np.min(spectrogramme))
                st.image(spectrogramme, caption="Spectrogramme", use_column_width=True)
                break
            wav_files = ["file1", "file2", "file3"] 
            dataset = tf.data.Dataset.from_tensor_slices(wav_files)
            dataset = dataset.map(lambda x: encode_single_sample(x, frame_length, frame_step, fft_length))
        

if selected == "Auto":
    pass