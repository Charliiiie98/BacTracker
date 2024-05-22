import streamlit as st
import pandas as pd

st.set_page_config(page_title="Datenbank", page_icon="🗂️", layout="wide")

# Load the Excel file
excel_file = 'statics/bakterien.xlsx'  # Name der Excel-Datei
sheet_name = 'bakterien'  # Name des Blatts, das du laden möchtest

# Read the excel file
df = pd.read_excel(excel_file, sheet_name=sheet_name)

# Sidebar für Suchfunktion und Filter
st.sidebar.title('Such- und Filteroptionen')

# Suchfunktion in der Sidebar
search_term = st.sidebar.text_input('Suche nach Begriff')

# Filter-Optionen in der Sidebar
filter_option = st.sidebar.selectbox(
    'Filter nach Bakterienform',
    ('Alle', 'Stäbchen', 'Kokken', 'kokkoide Stäbchen', 'Keulenform', 'Schraubenform', 'Sporenform')
)
def main():

    st.title('Bakterien Datenbank')

    tab1, tab2, tab3 = st.tabs(["Alle", "Negativ", "Positiv"])

    with tab1:
        filtered_df = df.copy()

        if search_term:
            filtered_df = filtered_df[filtered_df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]

        if filter_option != 'Alle':
            filtered_df = filtered_df[filtered_df['Form'] == filter_option]

        st.write("Datenbank-Inhalt:")
        show_df(filtered_df)

    with tab2:
        st.write("Negativ Bakterien:")
        negativ_df = filtered_df[filtered_df['Gram'] == 'Negativ']
        show_df(negativ_df)

    with tab3:
        st.write("Positiv Bakterien:")
        positiv_df = filtered_df[filtered_df['Gram'] == 'Positiv']
        show_df(positiv_df)

def show_df(df):
    # Pagination
    page = st.slider("Seite", 1, len(df) // 10 + 1)

    start_idx = (page - 1) * 10
    end_idx = min(len(df), start_idx + 10)

    st.write(df.iloc[start_idx:end_idx])

if __name__ == "__main__":
    main()
