import streamlit as st

def main():
    st.title('BacTracker')
    st.write('Welcome to your BacTracker App')
    st.page_link("home.py", label="Home", icon="🏠")
    st.page_link("pages/statistik.py", label="Statistik")
    st.page_link("pages/datenbank.py", label="Datenbank")
    
if __name__ == "__main__":
    main()
