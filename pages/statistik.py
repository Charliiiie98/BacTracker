import binascii
import streamlit as st
import pandas as pd
import bcrypt
from funktions.github_contents import GithubContents

# Constants
DATA_FILE_USERS = "MyLoginTable.csv"
DATA_FILE_STATS = "MyStatistikTable.csv"
USER_DATA_COLUMNS = ['username', 'name', 'password']
STAT_DATA_COLUMNS = ["Gattung", "Material", "Platten", "Pathogenität"]

# Streamlit configuration
st.set_page_config(page_title="Statistik", page_icon="📊", layout="wide")

def show():
    st.title("Login/Register")

def login_page():
    """Login an existing user."""
    st.title("Login")
    with st.form(key='login_form'):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            authenticate(username, password)

def register_page():
    """Register a new user."""
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
                new_user = pd.DataFrame([[new_username, new_name, hashed_password_hex]], columns=USER_DATA_COLUMNS)
                st.session_state.df_users = pd.concat([st.session_state.df_users, new_user], ignore_index=True)
                
                # Writes the updated dataframe to GitHub data repository
                st.session_state.github.write_df(DATA_FILE_USERS, st.session_state.df_users, "added new user")
                st.success("Registration successful! You can now log in.")

def authenticate(username, password):
    """Authenticate the user."""
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
    """Initialize or load the user dataframe."""
    if 'df_users' not in st.session_state:
        if st.session_state.github.file_exists(DATA_FILE_USERS):
            st.session_state.df_users = st.session_state.github.read_df(DATA_FILE_USERS)
        else:
            st.session_state.df_users = pd.DataFrame(columns=USER_DATA_COLUMNS)

def init_dataframe():
    """Initialize or load the statistic dataframe."""
    if 'df' not in st.session_state:
        try:
            if st.session_state.github.file_exists(DATA_FILE_STATS):
                st.session_state.df = st.session_state.github.read_df(DATA_FILE_STATS)
            else:
                st.session_state.df = pd.DataFrame(columns=STAT_DATA_COLUMNS)
        except Exception as e:
            st.error(f"Failed to load data from GitHub: {e}")
            st.session_state.df = pd.DataFrame(columns=STAT_DATA_COLUMNS)

def add_entry_in_sidebar():
    """Add a new entry to the DataFrame using pd.concat and calculate age."""
    new_entry = {
        STAT_DATA_COLUMNS[0]: st.sidebar.text_input(STAT_DATA_COLUMNS[0]),  # Name
        STAT_DATA_COLUMNS[1]: st.sidebar.text_input(STAT_DATA_COLUMNS[1]),
        STAT_DATA_COLUMNS[2]: st.sidebar.selectbox(STAT_DATA_COLUMNS[2], options=["", "Blutagar", "CET", "CIN", "CLED", "CNA",  "MCA", "MSA", "ALOA", "HEA"]),  # Replace with actual options
    }
    
    pathogen_status = st.sidebar.checkbox("Pathogenität", value=False)

    if st.sidebar.button("Add"):
        # Check whether all data is defined, otherwise show an error message
        for key, value in new_entry.items():
            if value == "":
                st.sidebar.error(f"Bitte ergänze das Feld '{key}'")
                return

        pathogen_status = "Pathogen" if pathogen_status else "Normal Flora"
        new_entry[STAT_DATA_COLUMNS[3]] = pathogen_status

        new_entry_df = pd.DataFrame([new_entry])
        st.session_state.df = pd.concat([st.session_state.df, new_entry_df], ignore_index=True)

        # Save the updated DataFrame to GitHub
        name = new_entry[STAT_DATA_COLUMNS[0]]
        msg = f"Add contact '{name}' to the file {DATA_FILE_STATS}"
        try:
            st.session_state.github.write_df(DATA_FILE_STATS, st.session_state.df, msg)
        except Exception as e:
            st.error(f"Failed to update GitHub repository: {e}")

def display_dataframe():
    if not st.session_state.df.empty:
        st.write(st.session_state.df)  # Use st.write() instead of st.dataframe()
    else:
        st.write("Keine Daten zum Anzeigen.")

def calculate_statistics():
    """Calculate statistics."""
    total_entries = len(st.session_state.df)
    total_pathogenic = st.session_state.df['Pathogenität'].value_counts().get('Pathogen', 0)  # Corrected column name here
    percent_pathogenic = (total_pathogenic / total_entries) * 100 if total_entries > 0 else 0
    return total_entries, total_pathogenic, percent_pathogenic

def main_statistik():
    """Main function for the statistik page."""
    if 'authentication' not in st.session_state or not st.session_state['authentication']:
        st.error("Please log in to access this page.")
        login_page()
        return
    
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
            data = st.session_state.df["Pathogenität"].value_counts().reset_index()  # Corrected column name here
            data.columns = ["Pathogenität", "Count"]
        elif plotx == "Platten":
            data = st.session_state.df["Platten"].value_counts().reset_index()
            data.columns = ["Platten", "Count"]
        elif plotx == "Material":
            data = st.session_state.df["Material"].value_counts().reset_index()
            data.columns = ["Material", "Count"]
        st.bar_chart(data.set_index(data.columns[0]))

def main():
    init_github()
    init_credentials()

    if 'authentication' not in st.session_state or not st.session_state['authentication']:
        st.sidebar.title("Authentication")
        login_button = st.sidebar.button("Login")
        register_button = st.sidebar.button("Register")

        # Check which button is pressed
        if login_button:
            st.session_state['current_page'] = "Login"
        elif register_button:
            st.session_state['current_page'] = "Register"

        # Display the appropriate page
        if 'current_page' in st.session_state:
            if st.session_state['current_page'] == "Login":
                login_page()
            elif st.session_state['current_page'] == "Register":
                register_page()
    else:
        main_statistik()

if __name__ == "__main__":
    main()
