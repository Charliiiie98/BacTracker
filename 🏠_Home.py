import streamlit as st

# Set page configuration
st.set_page_config(page_title="Home", page_icon="🏠", layout="wide")

# Define a function to handle the logout process
def logout():
    st.session_state['logged_in'] = False

# Define a function to set up the sidebar
def setup_sidebar():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = True
    if st.session_state['logged_in']:
        st.sidebar.button('Logout', on_click=logout)

# Define the main function for the home page
def home():
    setup_sidebar()
    if st.session_state['logged_in']:
        st.title('BacTracker')
        st.write('Welcome to your BacTracker App')
        st.image("statics/bakterien.jpeg", caption="Image of bacteria", use_column_width=True)
    else:
        st.write('Please log in to access the BacTracker App.')

# Define other pages if needed
def other_page():
    setup_sidebar()
    if st.session_state['logged_in']:
        st.title('Other Page')
        st.write('This is another page in your app.')
    else:
        st.write('Please log in to access this page.')

# Define a function to handle navigation
def main():
    # Create a sidebar menu
    menu = ['Home', 'Other Page']
    choice = st.sidebar.selectbox('Navigation', menu)

    # Navigate to the selected page
    if choice == 'Home':
        home()
    elif choice == 'Other Page':
        other_page()

# Run the main function
if __name__ == "__main__":
    main()
