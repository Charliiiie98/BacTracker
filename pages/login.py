import binascii
import streamlit as st
import pandas as pd
from funktions.github_contents import GithubContents
import bcrypt

# Set constants
DATA_FILE = "MyLoginTable.csv"
DATA_COLUMNS = ['username', 'name', 'password']

def login_page():
    """Login an existing user."""
    st.title("Login")
    with st.form(key='login_form'):
        st.session_state['username'] = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            authenticate(st.session_state.username, password)
            if st.session_state['authentication']:  # Redirect to statistik page upon successful login
                st.session_state['current_page'] = "statistik"
                st.experimental_set_query_params(page='statistik')


def register_page():
    """Register a new user."""
    st.title("Register")
    with st.form(key='register_form'):
        new_username = st.text_input("New Username")
        new_name = st.text_input("Name")
        new_password = st.text_input("New Password", type="password")
        if st.form_submit_button("Register"):
            hashed_password = bcrypt.hashpw(new_password.encode('utf8'), bcrypt.gensalt())  # Hash the password
            hashed_password_hex = binascii.hexlify(hashed_password).decode()  # Convert hash to hexadecimal string
            
            # Check if the username already exists
            if new_username in st.session_state.df_users['username'].values:
                st.error("Username already exists. Please choose a different one.")
                return
            else:
                new_user = pd.DataFrame([[new_username, new_name, hashed_password_hex]], columns=DATA_COLUMNS)
                st.session_state.df_users = pd.concat([st.session_state.df_users, new_user], ignore_index=True)
                
                try:
                    st.session_state.github.write_df(DATA_FILE, st.session_state.df_users, "added new user")
                    st.success("Registration successful! You can now log in.")
                    st.session_state['current_page'] = "Login"
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"Failed to update GitHub repository: {e}")

def authenticate(username, password):
    """Authenticate the user."""
    login_df = st.session_state.df_users
    login_df['username'] = login_df['username'].astype(str)

    if username in login_df['username'].values:
        stored_hashed_password = login_df.loc[login_df['username'] == username, 'password'].values[0]
        stored_hashed_password_bytes = binascii.unhexlify(stored_hashed_password)  # Convert hex to bytes
        
        # Check the input password
        if bcrypt.checkpw(password.encode('utf8'), stored_hashed_password_bytes): 
            st.session_state['authentication'] = True
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

def main():
    init_github()  # Initialize the GithubContents object
    init_credentials()  # Loads the credentials from the Github data repository

    if 'authentication' not in st.session_state:
        st.session_state['authentication'] = False

    if not st.session_state['authentication']:
        if 'current_page' not in st.session_state:
            st.session_state['current_page'] = "Login"

        # Display the appropriate page
        if st.session_state['current_page'] == "Login":
            login_page()
        elif st.session_state['current_page'] == "Register":
            register_page()
    else:
        st.experimental_set_query_params(page='statistik')  # Set the page parameter to 'statistik'

if __name__ == "__main__":
    main()
