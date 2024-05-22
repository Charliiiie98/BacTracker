import streamlit as st
from st_pages import hide_pages
from funktions.github_contents import GithubContents
import pandas as pd

# Hide specific pages from the app
hide_pages(['home', 'datenbank', 'statistik'])

# Constants for data file and columns
DATA_FILE = "MyLoginTable.csv"
DATA_COLUMNS = ['username', 'name', 'password']

def init_github():
    """Initialize the GithubContents object."""
    if 'github' not in st.session_state:
        st.session_state.github = GithubContents(
            st.secrets["github"]["owner"],
            st.secrets["github"]["repo"],
            st.secrets["github"]["token"])

def init_credentials():
    """Initialize or load the dataframe."""
    if 'df_users' not in st.session_state:
        if st.session_state.github.file_exists(DATA_FILE):
            st.session_state.df_users = st.session_state.github.read_df(DATA_FILE)
        else:
            st.session_state.df_users = pd.DataFrame(columns=DATA_COLUMNS)

def main():
    # Initialize GitHub connection and credentials
    init_github()
    init_credentials()

    st.title('BacTracker')
    st.write('Welcome to your BacTracker App')
    st.image("statics/bakterien.jpeg", caption="Image of bacteria", use_column_width=True)

    # Sidebar navigation
    st.sidebar.write("Navigation")
    st.sidebar.write("[Home](home.py) 🏠")
    st.sidebar.write("[Statistik](pages/muliuser_login.py) 📊")
    st.sidebar.write("[Datenbank](pages/datenbank.py)")

if __name__ == "__main__":
    main()
