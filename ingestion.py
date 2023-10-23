import streamlit as st
import pandas as pd
import sqlite3
import os

def ingestion():
    st.title("Importez vos données")
    uploaded_file = st.file_uploader("Téléchargez un fichier", type=["csv","xls","xlsx","sql","jpg","png"])

    if uploaded_file is not None:
        file_extension = os.path.splitext(uploaded_file.name)[1]

        if file_extension.lower() == ".csv":
            data = pd.read_csv(uploaded_file)
            st.dataframe(data)
            
        if file_extension.lower() in (".xls", ".xlsx"):
            data = pd.read_excel(uploaded_file)
            st.dataframe(data)

        if file_extension.lower() in (".jpg", ".png"):
            st.image(uploaded_file, caption="Votre data", use_column_width=True)
        
        if file_extension.lower() in (".sql"):
            sql_script = uploaded_file.read().decode('utf-8')

            # Create a SQLite in-memory database
            conn = sqlite3.connect(':memory:')
            cursor = conn.cursor()

            # Execute the SQL script
            cursor.executescript(sql_script)

            # Fetch all table names from the database
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            table_names = [table[0] for table in tables]

            if table_names:
                # Automatically display the first table
                first_table_name = table_names[0]
                query = f"SELECT * FROM {first_table_name}"
                df = pd.read_sql_query(query, conn)
                st.write(f"Data from table '{first_table_name}':")
                st.dataframe(df)