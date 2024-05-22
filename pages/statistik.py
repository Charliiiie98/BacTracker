import streamlit as st
import pandas as pd
from funktions.github_contents import GithubContents

DATA_FILE = "MyStatistikTable.csv"
DATA_COLUMNS = ["Gattung", "Material", "Platten", "Pathogen"]

st.set_page_config(page_title="Statistik", page_icon="📊", layout="wide")

def init_github():
    """Initialize the GithubContents object."""
    if 'github' not in st.session_state:
        st.session_state.github = GithubContents(
            st.secrets["github"]["owner"],
            st.secrets["github"]["repo"],
            st.secrets["github"]["token"])

def init_dataframe():
    """Initialize or load the dataframe."""
    if 'df' in st.session_state:
        pass
    elif st.session_state.github.file_exists(DATA_FILE):
        st.session_state.df = st.session_state.github.read_df(DATA_FILE)
    else:
        st.session_state.df = pd.DataFrame(columns=DATA_COLUMNS)

def add_entry_in_sidebar():
    """Add a new entry to the DataFrame using pd.concat and calculate age."""
    gattung = st.sidebar.text_input('Gattung')  # Gattung
    material = st.sidebar.text_input('Material')  # Material
    platten = st.sidebar.selectbox('Platten', ['', 'Option 1', 'Option 2', 'Option 3'])  # Platten
    pathogen = st.sidebar.selectbox('Platten', ['', 'Option 1', 'Option 2', 'Option 3'])  # Pathogen
    
    if gattung.strip() == "":
        st.sidebar.error("Bitte ergänze das Feld 'Gattung'")
        return
    if material.strip() == "":
        st.sidebar.error("Bitte ergänze das Feld 'Material'")
        return
    if platten == "":
        st.sidebar.error("Bitte wähle eine Option für 'Platten'")
        return
    
    new_entry = {
        'Gattung': gattung,
        'Material': material,
        'Platten': platten,
        'Pathogen': pathogen
    }
    st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([new_entry])], ignore_index=True)

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

def main_statistik():

    st.title("Statistik")

    init_dataframe()

    st.sidebar.header("Neuer Eintrag")
    gattung = st.sidebar.text_input("Gattung")
    material = st.sidebar.text_input("Material")
    
    platten_options = [""] + ["Blutagarplate", "CLED", "Hectoen", "Kochblutplatte", "Maconkey"]
    platten = st.sidebar.selectbox("Platten", platten_options)
    
    pathogen = st.sidebar.radio("Pathogen", ["normal Flora", "***Pathogen***"])
    add_button = st.sidebar.button("Hinzufügen")

    if add_button:  
        add_entry_in_sidebar(gattung, material, platten, pathogen)
        
    tab1, tab2 = st.tabs(["Tabelle", "Plot"])
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.header("Tabelle")
            display_dataframe()
        with col2:
            st.header("Anzahl")
            total_entries, total_pathogenic, percent_pathogenic = calculate_statistics()
            st.write(f"Gesamte Einträge: {total_entries}")
            st.write(f"Anzahl Pathoge: {total_pathogenic}")
            st.write(f"Prozentualer Anteil Pathoge: {percent_pathogenic:.2f}%")
    with tab2:
        st.header("Plot")
        plotx = st.radio("X-Achse", ["Pathogenität", "Platte", "Material"])
        if plotx == "Pathogenität":
            data = st.session_state.df["Pathogen"].value_counts().reset_index()
            data.columns = ["Pathogenität", "Count"]
        elif plotx == "Platte":
            data = st.session_state.df["Platten"].value_counts().reset_index()
            data.columns = ["Platte", "Count"]
        elif plotx == "Material":
            data = st.session_state.df["Material"].value_counts().reset_index()
            data.columns = ["Material", "Count"]
        st.bar_chart(data.set_index(data.columns[0]))

if __name__ == "__main__":
    main_statistik()
