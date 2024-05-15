import streamlit as st
import pandas as pd

st.set_page_config(page_title="Statistik", page_icon="📊", layout="wide")

def init_dataframe():
    """Initialize or load the dataframe."""
    if 'df' not in st.session_state:
        st.session_state.df = pd.DataFrame(columns=['Gattung', 'Material', 'Pathogen'])

def add_entry(gattung, material, pathogen):
    """Add a new entry to the DataFrame using pd.concat."""
    if gattung.strip() == "":
        st.sidebar.error("Bitte ergänze das Feld 'Gattung'")
        return
    if material.strip() == "":
        st.sidebar.error("Bitte ergänze das Feld 'Material'")
        return
    new_entry = pd.DataFrame([{'Gattung': gattung, 'Material': material, 'Pathogen': pathogen}])
    st.session_state.df = pd.concat([st.session_state.df, new_entry], ignore_index=True)

def display_dataframe():
    """Display the DataFrame in the app."""
    if not st.session_state.df.empty:
        st.dataframe(st.session_state.df)
    else:
        st.write("Keine Daten zum Anzeigen.")

def calculate_statistics():
    """Calculate statistics."""
    total_entries = len(st.session_state.df)
    total_pathogenic = st.session_state.df['Pathogen'].value_counts().get('***Pathogen***', 0)
    percent_pathogenic = (total_pathogenic / total_entries) * 100 if total_entries > 0 else 0
    return total_entries, total_pathogenic, percent_pathogenic

def main():
    st.title("Statistik")

    init_dataframe()

    with st.sidebar:
        st.header("Neuer Eintrag")
        gattung = st.text_input("Gattung")
        material = st.text_input("Material")
        pathogen = st.radio("Pathogen", ["normal Flora", "***Pathogen***"])
        add_button = st.button("Hinzufügen")

    if add_button:  
        add_entry(gattung, material, pathogen)

    col1, col2 = st.columns(2)

    with col1:
        st.header("Liste")
        display_dataframe()

    with col2:
        st.header("Anzahl")
        total_entries, total_pathogenic, percent_pathogenic = calculate_statistics()
        st.write(f"Gesamte Einträge: {total_entries}")
        st.write(f"Anzahl Pathoge: {total_pathogenic}")
        st.write(f"Prozentualer Anteil Pathoge: {percent_pathogenic:.2f}%")

if __name__ == "__main__":
    main()
