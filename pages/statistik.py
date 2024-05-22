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
    if 'df' not in st.session_state:
        try:
            if st.session_state.github.file_exists(DATA_FILE):
                st.session_state.df = st.session_state.github.read_df(DATA_FILE)
            else:
                st.session_state.df = pd.DataFrame(columns=DATA_COLUMNS)
        except Exception as e:
            st.error(f"Failed to load data from GitHub: {e}")
            st.session_state.df = pd.DataFrame(columns=DATA_COLUMNS)

def add_entry_in_sidebar():
    """Add a new entry to the DataFrame using pd.concat and calculate age."""
    new_entry = {
        DATA_COLUMNS[0]: st.sidebar.text_input(DATA_COLUMNS[0]),  # Name
        DATA_COLUMNS[1]: st.sidebar.text_input(DATA_COLUMNS[1]),
        DATA_COLUMNS[2]: st.sidebar.selectbox(DATA_COLUMNS[2], options=["Option1", "Option2"]),  # Replace with actual options
        DATA_COLUMNS[3]: st.sidebar.radio(DATA_COLUMNS[3], options=["normal Flora", "pathogen"]) # Replace with actual options
    }
    
    # Check whether all data is defined, otherwise show an error message
    for key, value in new_entry.items():
        if value == "":
            st.sidebar.error(f"Bitte ergänze das Feld '{key}'")
            return

    if st.sidebar.button("Add"):
        new_entry_df = pd.DataFrame([new_entry])
        st.session_state.df = pd.concat([st.session_state.df, new_entry_df], ignore_index=True)

        # Save the updated DataFrame to GitHub
        name = new_entry[DATA_COLUMNS[0]]
        msg = f"Add contact '{name}' to the file {DATA_FILE}"
        try:
            st.session_state.github.write_df(DATA_FILE, st.session_state.df, msg)
        except Exception as e:
            st.error(f"Failed to update GitHub repository: {e}")

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
    init_github()
    init_dataframe()
    add_entry_in_sidebar()
    
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
            st.write(f"Anzahl Pathogen: {total_pathogenic}")
            st.write(f"Prozentualer Anteil Pathogen: {percent_pathogenic:.2f}%")
            
    with tab2:
        st.header("Plot")
        plotx = st.radio("X-Achse", ["Pathogenität", "Platten", "Material"])
        if plotx == "Pathogenität":
            data = st.session_state.df["Pathogen"].value_counts().reset_index()
            data.columns = ["Pathogenität", "Count"]
        elif plotx == "Platten":
            data = st.session_state.df["Platten"].value_counts().reset_index()
            data.columns = ["Platten", "Count"]
        elif plotx == "Material":
            data = st.session_state.df["Material"].value_counts().reset_index()
            data.columns = ["Material", "Count"]
        st.bar_chart(data.set_index(data.columns[0]))

if __name__ == "__main__":
    main_statistik()

