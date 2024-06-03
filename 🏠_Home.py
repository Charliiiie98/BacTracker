import streamlit as st
from st_pages import hide_pages

st.set_page_config(page_title="Home", page_icon="🏠", layout="wide")

hide_pages(['login'])

def main():
    st.title('BacTracker')
    st.write('Welcome to your BacTracker App')
    st.image("statics/bakterien.jpeg", use_column_width=True)

if __name__ == "__main__":
        main()
