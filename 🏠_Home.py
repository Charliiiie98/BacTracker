import streamlit as st

st.set_page_config(page_title="Home", page_icon="🏠", layout="wide")

def main():
    st.title('BacTracker')
    st.write('Welcome to your BacTracker App')

    # CSS for setting background image
    st.markdown(
        """
        <style>
        .stApp {
            background-image: ('statics/bakterien.jpeg');
            background-size: cover;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
