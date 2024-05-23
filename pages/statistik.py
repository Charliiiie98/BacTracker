def main_statistik():
    st.title("Statistik")
    init_github()
    init_credentials()
    init_dataframe()  # Initialize the dataframe
    
    if not st.session_state['authentication']:
        login_page()
        return
    
    add_entry_in_sidebar()
    
    tab1, tab2 = st.columns(2)
    
    with tab1:
        st.header("Tabelle")
        if not st.session_state.df.empty:  # Check if the dataframe is not empty
            display_dataframe()  # Display dataframe
        else:
            st.write("Keine Daten zum Anzeigen.")
    
    with tab2:
        st.header("Anzahl")
        if not st.session_state.df.empty:  # Check if the dataframe is not empty
            total_entries, total_pathogenic, percent_pathogenic = calculate_statistics()
            st.write(f"Gesamte Einträge: {total_entries}")
            st.write(f"Anzahl Pathogen: {total_pathogenic}")
            st.write(f"Prozentualer Anteil Pathogen: {percent_pathogenic:.2f}%")
        else:
            st.write("Keine Daten zum Anzeigen.")

    st.header("Plot")
    plotx = st.radio("X-Achse", ["Pathogenität", "Platten", "Material"])
    if not st.session_state.df.empty:  # Check if the dataframe is not empty
        if plotx == "Pathogenität":
            data = st.session_state.df["Pathogenität"].value_counts().reset_index()  # Corrected column name here
            data.columns = ["Pathogenität", "Count"]
        elif plotx == "Platten":
            data = st.session_state.df["Platten"].value_counts().reset_index()
            data.columns = ["Platten", "Count"]
        elif plotx == "Material":
            data = st.session_state.df["Material"].value_counts().reset_index()
            data.columns = ["Material", "Count"]
        st.bar_chart(data.set_index(data.columns[0]))
    else:
        st.write("Keine Daten zum Anzeigen.")

if __name__ == "__main__":
    main_statistik()

