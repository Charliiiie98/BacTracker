import streamlit as st

st.set_page_config(page_title="Home", page_icon="🏠", layout="wide")

def main():
    init_github()
    init_credentials()
    st.title('BacTracker')
    st.write('Welcome to your BacTracker App')
    st.image("statics/bakterien.jpeg", caption="Image of bacteria", use_column_width=True)

if __name__ == "__main__":
        main()
