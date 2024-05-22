import streamlit as st
from st_pages import hide_pages
from github_contents import GithubContents

hide_pages(['home', 'datenbank', 'statistik'])
def main():
    st.title('BacTracker')
    st.write('Welcome to your BacTracker App')
    st.image("statics/bakterien.jpeg", caption="Image of bacteria", use_column_width=True)
    st.sidebar.page_link("home.py", label="Home", icon="🏠")
    st.sidebar.page_link("pages/statistik.py", label="Statistik", icon="📊")
    st.sidebar.page_link("pages/datenbank.py", label="Datenbank")

if __name__ == "__main__":
    main()
