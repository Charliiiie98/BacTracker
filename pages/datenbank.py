import streamlit as st
import pandas as pd

# Title of the web app
st.title('Excel Datenbank Darstellung')

# Load the Excel file
excel_file = 'pages/bakterien.xlsx'  # Name der Excel-Datei
sheet_name = 'bakterien'  # Name des Blatts, das du laden möchtest

# Read the excel file
df = pd.read_excel(excel_file, sheet_name=sheet_name)

# Sidebar für Suchfunktion und Filter
st.sidebar.title('Such- und Filteroptionen')

# Suchfunktion in der Sidebar
search_term = st.sidebar.text_input('Suche nach Begriff')

# Filter-Optionen in der Sidebar
filter_option = st.sidebar.radio(
    'Filter nach Bakterienform',
    ('Alle', 'Stäbchen', 'Kokken', 'kokkoide Stäbchen', 'Keulenform', 'Schraubenform', 'Sporenform')
)

def main():

    tab1, tab2, tab3 = st.tabs(["Alle", "Negativ", "Positiv"])

    with tab1:
        filtered_df = df.copy()

        if search_term:
            filtered_df = filtered_df[filtered_df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]

        if filter_option != 'Alle':
            filtered_df = filtered_df[filtered_df['Form'] == filter_option]

        st.write("Datenbank-Inhalt:")
        st.dataframe(filtered_df, width=1000, height=2600)

    with tab2:
        st.write("Negativ Bakterien:")
        negativ_df = filtered_df[filtered_df['Gram'] == 'Negativ']
        st.dataframe(negativ_df, width=1000, height=600)

    with tab3:
        st.write("Positiv Bakterien:")
        positiv_df = filtered_df[filtered_df['Gram'] == 'Positiv']
        st.dataframe(positiv_df, width=1000, height=600)
if __name__ == "__main__":
    main()

