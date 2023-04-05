import streamlit as st

import zyl.visualize as vis_zyl

# st.set_page_config(layout="wide")


def chart_seasonal_temperature():
    st.title("Temperautre has Increased a Lot in Winter")
    st.altair_chart(vis_zyl.plot_seasonal_temperature())
    st.write("""Global warming is a well known issue right now. This visualization shows though 
    average temperature has increased for all seasons, winter increased much faster than other seasons, which reaches
      0.024 \N{DEGREE SIGN}F per year. As skiing is most in winter, it will be affected more seriously than we think.
      In addtion, from the graph, temperature increases faster than before in recent decades. 
      Interact with above visualizations to find temperature in each year.""")

def chart_snow_cover():
    st.title("Snow Cover is Slowly Decreasing")
    st.altair_chart(vis_zyl.plot_snow_cover())
    st.write("""We can see the year average snow cover drops a little bit. Snow cover varies a lot in different months in a year. 
        Snow cover varies a lot in different month over a year. We find that snow cover drops quickly across years in summer (June, July and August).
        In winter (Deecember, January, February), snow cover does not vary a lot across years. Explore the data by choosing the month you are interested.
    """)

def chart_snow_duration():
    st.title("Snow Season Length Decreases two weeks from 1972")
    st.altair_chart(vis_zyl.plot_snow_duration())
    st.write(
        """
            Snow season length is the number of days between the first snow and last snow in a year. The regression line clearly shows that the 
            season length drops quickly. Starting from 1972, it has decreased approximately two weeks, which will affect ski industry a lot.
        """
    )
    

def chart_snowfall():
    st.title("Snowfall Temprorily Maintains Thanks to High Precipitation")
    st.altair_chart(vis_zyl.plot_snowfall())
    st.write()
    st.altair_chart(vis_zyl.plot_snowfall_precipitation())

visualizations = [chart_seasonal_temperature, chart_snow_cover, chart_snow_duration, chart_snowfall]
viz_options = ["Seasonal Temperature", "Snow Cover", "Snow Season Length", "Snowfall by Geography"]

def main():
    st.set_page_config(layout="wide")

    state = _get_state()

        # Display the current visualization
    visualizations[state.current_viz]()

    st.sidebar.title("How Can Global Warming Impact US Ski Industry")
    with st.sidebar:
        selected_viz = st.radio(
            "Experience through our visualizations:",
            options=viz_options,
            index=state.current_viz,
            key="nav_bar"
        )

    if state.current_viz != viz_options.index(selected_viz):
        state.current_viz = viz_options.index(selected_viz)
        st.experimental_rerun()
    

    # Add arrow buttons for navigation
    col1, col2, col3 = st.columns([2, 9, 2])
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


def _get_state():
    if "state" not in st.session_state:
        st.session_state.state = SimpleNamespace(current_viz=0)
    return st.session_state.state

class SimpleNamespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def sync(self):
        pass

if __name__ == "__main__":
    main()
