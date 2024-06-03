import streamlit as st

# Set page configuration
st.set_page_config(page_title="Home", page_icon="🏠", layout="wide")

# Define a function to handle the logout process
def logout():
    st.session_state['logged_in'] = False

# Define the main function
def main():
    # Check if the user is logged in
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = True

    if st.session_state['logged_in']:
        st.sidebar.button('Logout', on_click=logout)
        st.title('BacTracker')
        st.write('Welcome to your BacTracker App')
        st.image("statics/bakterien.jpeg", caption="Image of bacteria", use_column_width=True)
    else:
        st.sidebar.write('You have been logged out.')
        st.write('Please log in to access the BacTracker App.')

# Run the main function
if __name__ == "__main__":
    main()
