import binascii
import streamlit as st
import pandas as pd
import bcrypt
from funktions.github_contents import GithubContents

# Constants
DATA_FILE = "MyStatistikTable.csv"
DATA_COLUMNS = ["Gattung", "Material", "Platten", "Pathogenität"]

def show():
    st.title("Login/Register")

def login_page():
    """ Login an existing user. """
    st.title("Login")
    with st.form(key='login_form'):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            authenticate(username, password)

def register_page():
    """ Register a new user. """
    st.title("Register")
    with st.form(key='register_form'):
        new_username = st.text_input("New Username")
        new_name = st.text_input("Name")
        new_password = st.text_input("New Password", type="password")
        if st.form_submit_button("Register"):
            hashed_password = bcrypt.hashpw(new_password.encode('utf8'), bcrypt.gensalt())
            hashed_password_hex = binascii.hexlify(hashed_password).decode()
            
            # Check if the username already exists
            if new_username in st.session_state.df_users['username'].values:
                st.error("Username already exists. Please choose a different one.")
                return
            else:
                new_user = pd.DataFrame([[new_username, new_name, hashed_password_hex]], columns=DATA_COLUMNS)
                st.session_state.df_users = pd.concat([st.session_state.df_users, new_user], ignore_index=True)
                
                # Writes the updated dataframe to GitHub data repository
                st.session_state.github.write_df(DATA_FILE, st.session_state.df_users, "added new user")
                st.success("Registration successful! You can now log in.")

def authenticate(username, password):
    """
    Authenticate the user.

    Parameters:
    username (str): The username to authenticate.
    password (str): The password to authenticate.
    """
    login_df = st.session_state.df_users
    login_df['username'] = login_df['username'].astype(str)

    if username in login_df['username'].values:
        stored_hashed_password = login_df.loc[login_df['username'] == username, 'password'].values[0]
        stored_hashed_password_bytes = binascii.unhexlify(stored_hashed_password)
        
        # Check the input password
        if bcrypt.checkpw(password.encode('utf8'), stored_hashed_password_bytes): 
            st.session_state['authentication'] = True
            st.session_state['username'] = username
            st.success('Login successful')
            st.experimental_rerun()
        else:
            st.error('Incorrect password')
    else:
        st.error('Username not found')

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

def main_statistik():
    st.title("Statistik")
    init_github()
    init_credentials()
    
    if not st.session_state['authentication']:
        login_page()
        return
    
    # Rest of your existing code for the statistics page
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
            data = st.session_state.df["Pathogenität"].value_counts().reset_index()  # Corrected column name here
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


