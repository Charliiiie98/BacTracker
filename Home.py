import streamlit as st

def main():
    st.title('BacTracker')
    st.write('Welcome to your BacTracker App')
    st.page_link("home.py", label="Home", icon="🏠")
    st.page_link("Pages/Statistik.py", label="Statistik")
    st.page_link("Pages/Datenbank.py", label="Datenbank")

    if st.button("Home"):
        st.switch_page("home.py")
    if st.button("Statistik"):
        st.switch_page("Pages/Statistik.py")
    if st.button("Datenbank"):
        st.switch_page("Pages/Datenbank.py")
    
if __name__ == "__main__":
    main()
