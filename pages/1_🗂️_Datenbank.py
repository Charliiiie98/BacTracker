import streamlit as st
import pandas as pd
from st_pages import hide_pages

st.set_page_config(page_title="Datenbank", page_icon="🗂️", layout="wide")

excel_file = 'statics/bakterien.xlsx'  # Name der Excel-Datei
sheet_name = 'bakterien'  # Name des Blatts, das du laden möchtest

df = pd.read_excel(excel_file, sheet_name=sheet_name)

def sidebar():
    st.sidebar.title('Such- und Filteroptionen')

    search_term = st.sidebar.text_input('Suche nach Begriff')

    form_option = st.sidebar.selectbox(
        'Filter nach Bakterienform',
        ('Alle', 'Kokken', 'kokkoide Stäbchen', 'Keulenform', 'nicht einteilbar', 'Schraubenform', 'Sporenform', 'Stäbchen')
    )

    characterization_options = ['α-Hämolyse', 'β-Hämolyse', 'Aesculin +' 'CAMP +', 'Gas +', 'Halbsäurefest', 'Hippurat +', 'Indol +',
                                'Kapsel', 'Katalase +', 'Katalase -', 'Koagulase +', 'Koagulase -', 'KOH +', 'Kultur', 'Lac +', 'Lac -',
                                'nicht kultivierbar', 'Oxidase +', 'Oxidase -', 'PCR', ' Pyr +', 'Säurefest', 'Serologie', 'Urease +']
    
    selected_characterizations = st.sidebar.multiselect('Filter nach Charakteristik', characterization_options)

    return search_term, form_option, selected_characterizations
    
hide_pages(['login'])

def main():
    # Title of the web app
    st.title('Bakterien Datenbank')
    
    tab1, tab2, tab3 = st.tabs(["Alle", "Negativ", "Positiv"])

    search_term, form_option, selected_characterizations = sidebar()

    with tab1:
        filtered_df = df.copy()

        # Apply search term filter
        if search_term:
            filtered_df = filtered_df[filtered_df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]

        # Apply bacteria form filter
        if form_option != 'Alle':
            filtered_df = filtered_df[filtered_df['Form'] == form_option]

        # Apply characterizations filter
        if selected_characterizations:
            filtered_df = filtered_df[
                filtered_df.apply(
                    lambda row: all(char in ' '.join([str(row['Charakteristik1']), str(row['Charakteristik2']), str(row['Charakteristik3'])]) for char in selected_characterizations), 
                    axis=1
                )
            ]

        st.write("Datenbank-Inhalt:")
        st.markdown(filtered_df.to_html(index=False, escape=False), unsafe_allow_html=True)  # Convert DataFrame to HTML and render using st.markdown

    with tab2:
        st.write("Negativ Bakterien:")
        negativ_df = filtered_df[filtered_df['Gram'] == 'Negativ']
        st.markdown(negativ_df.to_html(index=False, escape=False), unsafe_allow_html=True)  # Convert DataFrame to HTML and render using st.markdown

    with tab3:
        st.write("Positiv Bakterien:")
        positiv_df = filtered_df[filtered_df['Gram'] == 'Positiv']
        st.markdown(positiv_df.to_html(index=False, escape=False), unsafe_allow_html=True)  # Convert DataFrame to HTML and render using st.markdown

if __name__ == "__main__":
    main()
