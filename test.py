import streamlit as st
from types import SimpleNamespace

def main():
    st.set_page_config(layout="wide")
    state = _get_state()

    # Add your visualizations as separate functions
    def visualization_1():
        st.write("### Visualization 1")
        st.write("This is the first visualization.")
        # Add the code for your first visualization here

    def visualization_2():
        st.write("### Visualization 2")
        st.write("This is the second visualization.")
        # Add the code for your second visualization here

    def visualization_3():
        st.write("### Visualization 3")
        st.write("This is the third visualization.")
        # Add the code for your third visualization here

    
    # A list of all visualization functions
    visualizations = [visualization_1, visualization_2, visualization_3]

    # Add a navigation bar in the sidebar
    st.sidebar.title("Navigation")
    viz_options = ["Visualization 1", "Visualization 2", "Visualization 3"]
    
    with st.sidebar:
        selected_viz = st.radio(
            "Choose a visualization:",
            options=viz_options,
            index=state.current_viz,
            key="nav_bar"
        )

    if state.current_viz != viz_options.index(selected_viz):
        state.current_viz = viz_options.index(selected_viz)
        st.experimental_rerun()

    
    # Add arrow buttons for navigation at the top of the page
    col1, col2, col3 = st.columns([2, 5, 2])
    with col1:
        if st.button("← Previous"):
            state.current_viz -= 1
            state.current_viz %= len(visualizations)
            st.experimental_rerun()

    with col3:
        if st.button("Next →"):
            state.current_viz += 1
            state.current_viz %= len(visualizations)
            st.experimental_rerun()


    # Display the current visualization
    visualizations[state.current_viz]()

def _get_state():
    if "state" not in st.session_state:
        st.session_state.state = SimpleNamespace(current_viz=0)
    return st.session_state.state

if __name__ == "__main__":
    main()