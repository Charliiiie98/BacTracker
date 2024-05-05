import streamlit as st

def main():
    st.title('BacTracker')
    st.write('Welcome to your BacTracker App')

    # Page links
    if st.button("Home"):
        st.experimental_set_query_params(page="home")
    if st.button("Statistik"):
        st.experimental_set_query_params(page="statistik")
    if st.button("Datenbank"):
        st.experimental_set_query_params(page="datenbank")

    # Handle pages
    query_params = st.query_params
    page = query_params.get("page", ["home"])[0]

    if page == "home":
        st.title("Home")
        # Add content for home page
    elif page == "statistik":
        st.title("Statistik")
        # Add content for statistics page
    elif page == "datenbank":
        st.title("Datenbank")
        # Add content for database page

if __name__ == "__main__":
    main()
