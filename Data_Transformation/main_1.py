import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder, OneHotEncoder
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.decomposition import PCA
import os

df = pd.read_csv("C:/Users/INFOTECH/Downloads/Compressed/creditcard.csv")
normalised_data=None
selected = option_menu(
menu_title=None,
options=["Normaliser", "Agréger"],  
menu_icon="cast", 
default_index=0,  
orientation="horizontal",
styles={
    "container": {"padding": "0!important","color": "black", "background-color": "#fafafa"},
    "icon": {"color": "orange", "font-size": "25px"},
    "nav-link": {
        "font-size": "25px",
        "color": "black",
        "text-align": "center",
        "margin": "0px"
        },
    "nav-link-selected": {"background-color": "green","color": "#FFE4E1"},
            },
        )

if selected == "Normaliser":
    col1, col2 = st.columns(2)

    with col1:
        normalization = st.selectbox("Variables Quantitatives:", ["None", "StandardScaler", "MinMaxScaler", "Auto"])
        st.write("Vous avez sélectionné :", normalization)
        if normalization == "StandardScaler":
            scaler = StandardScaler()
            df[df.select_dtypes(exclude='object').columns] = scaler.fit_transform(df.select_dtypes(exclude='object'))
        elif normalization == "MinMaxScaler" or normalization== "Auto":
            scaler = MinMaxScaler()
            df[df.select_dtypes(exclude='object').columns] = scaler.fit_transform(df.select_dtypes(exclude='object'))


    with col2:
        categorical_encoding = st.selectbox("Variables Qualtitatives:", ["None", "LabelEncoder", "OneHotEncoder", "Auto"])
        if categorical_encoding == "LabelEncoder":
            label_encoder = LabelEncoder()
            for col in df.select_dtypes(include='object'):
                df[col] = label_encoder.fit_transform(df[col])
        elif categorical_encoding == "OneHotEncoder" or categorical_encoding=="Auto":
            categorical_columns = df.select_dtypes(include='object').columns
            df = pd.get_dummies(df, columns=categorical_columns)
        st.write("Vous avez sélectionné :", categorical_encoding)

    st.write(" Data Normalisé:")
    normalised_data = df.copy()  # Update the global variable with normalized data
    st.dataframe(normalised_data.head())
    normalised_data.to_csv("ff.csv")

if selected == "Agréger":

    if os.path.isfile("ff.csv"):
        normalised_data = pd.read_csv("ff.csv", index_col=0)
        st.write("Data Normalisé:  ")
        st.dataframe(normalised_data.head())
        print("len 1",len(normalised_data))
        print("len 2",len(normalised_data.columns))

        choice = st.radio("Choose a Data Transformation Method:", ("Feature Selection", "auto"))
        if choice == "Feature Selection":
            # Let the user select the columns to maintain
            selected_columns = st.multiselect("Select columns to maintain:", normalised_data.columns)
            normalised_data_filtered = normalised_data[selected_columns]
            st.write("Filtered Data:")
            st.dataframe(normalised_data_filtered)
        elif choice == "auto":
            # User's choice for PCA method
            pca_method = st.radio("Choose PCA Method:", ("Choose Number of Components", "Auto"))
            if pca_method == "Choose Number of Components":
                # Allow the user to choose the number of components with a slider
                num_components = st.slider("Select Number of Components:", min_value=1, max_value=len(normalised_data.columns)-1)
                
                # Apply PCA
                pca = PCA(n_components=num_components)
                X_pca = pca.fit_transform(normalised_data)
                normalised_data_pca = pd.DataFrame(X_pca, columns=[f"PC{i+1}" for i in range(num_components)])
                
                # Display the PCA-transformed data
                st.write("PCA-transformed Data:")
                st.dataframe(normalised_data_pca.head())

            elif pca_method == "Auto":
                # Check if the number of samples is greater than or equal to the number of features
                if len(normalised_data) >= len(normalised_data.columns):
                    pca = PCA(n_components=0.95)
                    X_pca = pca.fit_transform(normalised_data)
                    normalised_data_pca = pd.DataFrame(data=X_pca)

                    # Display the PCA-transformed data
                    st.write("PCA-transformed Data:")
                    st.dataframe(normalised_data_pca.head())
                else:
                    st.write("The number of samples is less than the number of features. Cannot apply PCA with 'mle'.")
    else : 
        st.write("You have to normalise first")

