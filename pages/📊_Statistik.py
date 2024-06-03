import binascii
import streamlit as st
import pandas as pd
import bcrypt
from funktions.github_contents import GithubContents
from st_pages import hide_pages
# Constants
DATA_FILE_USERS = "MyLoginTable.csv"
DATA_FILE_STATS = "MyStatistikTable.csv"
USER_DATA_COLUMNS = ['username', 'name', 'password']
STAT_DATA_COLUMNS = ["Gattung", "Material", "Platten", "Pathogenität", 'username']
# Streamlit configuration
st.set_page_config(page_title="Statistik", page_icon="📊", layout="wide")
def authenticate(username, password):
    """Authenticate the user."""
    login_df = st.session_state.df_users
    login_df['username'] = login_df['username'].astype(str)
    if username in login_df['username'].values:
        stored_hashed_password = login_df.loc[login_df['username'] == username, 'password'].values[0]
        stored_hashed_password_bytes = binascii.unhexlify(stored_hashed_password)
        
        if bcrypt.checkpw(password.encode('utf8'), stored_hashed_password_bytes): 
            st.session_state['authentication'] = True
            st.session_state['username'] = username
            st.success('Login successful')
            st.experimental_rerun()
        else:
            st.error('Incorrect password')
    else:
        st.error('Username not found')
def login_page():
    """Login an existing user."""
    st.title("Login")
    with st.form(key='login_form'):
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        submit_button = st.form_submit_button("Login")
        if submit_button:
            authenticate(username, password)
def register_page():
    """Register a new user."""
    st.title("Register")
    with st.form(key='register_form'):
        new_username = st.text_input("New Username", key="register_username")
        new_name = st.text_input("Name", key="register_name")
        new_password = st.text_input("New Password", type="password", key="register_password")
        submit_button = st.form_submit_button("Register")
        if submit_button:
            hashed_password = bcrypt.hashpw(new_password.encode('utf8'), bcrypt.gensalt())
            hashed_password_hex = binascii.hexlify(hashed_password).decode()
            
            if new_username in st.session_state.df_users['username'].values:
                st.error("Username already exists. Please choose a different one.")
                return
            else:
                new_user = pd.DataFrame([[new_username, new_name, hashed_password_hex]], columns=USER_DATA_COLUMNS)
                st.session_state.df_users = pd.concat([st.session_state.df_users, new_user], ignore_index=True)
                
                st.session_state.github.write_df(DATA_FILE_USERS, st.session_state.df_users, "added new user")
                st.success("Registration successful! Redirecting to login page...")
                st.session_state['current_page'] = "Login"
                st.experimental_rerun()
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
    """Add a new entry to the DataFrame."""
    new_entry = {}
    for i, column in enumerate(STAT_DATA_COLUMNS):
        unique_key = f"{column}_{i}_entry"
        if column != 'username' and column != 'Pathogenität':
            if column == 'Platten':
                new_entry[column] = st.sidebar.selectbox(column, options=["Blutagar", "CET", "CLED", "CNA", "HEA", "Kochblutagar", "MCA", "MSA"], key=unique_key)
            else:
                new_entry[column] = st.sidebar.text_input(column, key=unique_key)
    
    pathogen_status = st.sidebar.checkbox("Pathogenität", value=False, key="pathogen_status")
    if st.sidebar.button("Add", key="add_button"):
        for key, value in new_entry.items():
            if value == "":
                st.sidebar.error(f"Bitte ergänze das Feld '{key}'")
                return
        pathogen_status = "Pathogen" if pathogen_status else "Normal Flora"
        new_entry['Pathogenität'] = pathogen_status
        new_entry['username'] = st.session_state['username']
        new_entry_df = pd.DataFrame([new_entry])
        st.session_state.df = pd.concat([st.session_state.df, new_entry_df], ignore_index=True)
        name = new_entry[STAT_DATA_COLUMNS[0]]
        msg = f"Add entry '{name}' to the file {DATA_FILE_STATS}"
        try:
            st.session_state.github.write_df(DATA_FILE_STATS, st.session_state.df, msg)
        except Exception as e:
            st.error(f"Failed to update GitHub repository: {e}")
def display_dataframe():
    """Display the DataFrame for the authenticated user."""
    if not st.session_state.df.empty:
        username = st.session_state.get('username')
        if 'username' in st.session_state.df.columns:
            user_entries = st.session_state.df[st.session_state.df['username'] == username]
            if not user_entries.empty:
                user_entries_without_username = user_entries.drop(columns=['username'])
                st.write(user_entries_without_username)
            else:
                st.write("You have not added any entries yet.")
        else:
            st.error("The 'username' column does not exist in the DataFrame.")
    else:
        st.write("No data to display.")
def calculate_statistics(user_df):
    """Calculate statistics for the authenticated user."""
    total_entries = len(user_df)
    total_pathogenic = user_df['Pathogenität'].value_counts().get('Pathogen', 0)
    percent_pathogenic = (total_pathogenic / total_entries) * 100 if total_entries > 0 else 0
    return total_entries, total_pathogenic, percent_pathogenic

def logout():
    """Logout the user."""
    st.session_state['authentication'] = False
    st.session_state['username'] = None
    st.experimental_rerun()
    
hide_pages(['login'])

def main():
    """Main function to control the app flow."""
    init_github()
    init_credentials()
    if 'authentication' not in st.session_state:
        st.session_state['authentication'] = False
    if not st.session_state['authentication']:
        st.sidebar.title("Authentication")
        login_button = st.sidebar.button("Login", key="login_button")
        register_button = st.sidebar.button("Register", key="register_button")
        if login_button:
            st.session_state['current_page'] = "Login"
        elif register_button:
            st.session_state['current_page'] = "Register"
        if 'current_page' in st.session_state:
            if st.session_state['current_page'] == "Login":
                login_page()
            elif st.session_state['current_page'] == "Register":
                register_page()
        return
    
    st.sidebar.title("Navigation")
    add_entry_in_sidebar()
    
    st.sidebar.write("")  # Empty string to add some space
    st.sidebar.write("")  # Empty string to add more space if needed
    st.sidebar.write("")  # You can add more lines for additional space
    logout_button = st.sidebar.button("Logout", key="logout_button")
    if logout_button:
        logout()
    
    st.title("Statistik")
    init_dataframe()
    
    username = st.session_state.get('username')  # Changed to use .get() for safe access
    user_df = st.session_state.df[st.session_state.df['username'] == username]

    col1, col2 = st.columns(2)
        
    with col1:
        st.header("Tabelle")
        display_dataframe()
        
    with col2:
        st.header("Anzahl")
        total_entries, total_pathogenic, percent_pathogenic = calculate_statistics(user_df)
        st.write(f"Gesamte Einträge: {total_entries}")
        st.write(f"Anzahl Pathogen: {total_pathogenic}")
        st.write(f"Prozentualer Anteil Pathogen: {percent_pathogenic:.2f}%")
        st.header("Plot")
        plotx = st.radio("X-Achse", ["Pathogenität", "Platten", "Material"])
            if plotx == "Pathogenität":
                data = st.session_state.df["Pathogenität"].value_counts().reset_index()
                data.columns = ["Pathogenität", "Count"]
            elif plotx == "Platten":
                data = st.session_state.df["Platten"].value_counts().reset_index()
                data.columns = ["Platten", "Count"]
            elif plotx == "Material":
                data = st.session_state.df["Material"].value_counts().reset_index()
                data.columns = ["Material", "Count"]
            st.bar_chart(data.set_index(data.columns[0]))


if __name__ == "__main__":
    main()
