import streamlit as st

import zyl.visualize as vis_zyl
import cxw.visualize as vis_cxw
import hhy.visualize as vis_hhy
import ydm.visualize as vis_ydm

# st.set_page_config(layout="wide")


def chart_seasonal_temperature():
    st.title("Temperature has Increased a Lot in Winter")
    st.altair_chart(vis_zyl.plot_seasonal_temperature())
    st.write("""Global warming is a well known issue right now. This visualization shows though 
    average temperature has increased for all seasons, winter increased much faster than other seasons, which reaches
      0.024 \N{DEGREE SIGN}F per year. As skiing is most in winter, it will be affected more seriously than we think.
      In addtion, from the graph, temperature increases faster than before in recent decades. 
      Interact with above visualizations to find temperature in each year.""")
    st.markdown('[Data Source: National Centers for Environmental Information](https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/national/time-series)')


def chart_snow_cover():
    st.title("Snow Cover is Slowly Decreasing")
    st.altair_chart(vis_zyl.plot_snow_cover())
    st.write("""We can see the year average snow cover drops a little bit. Snow cover varies a lot in different months in a year. 
        Snow cover varies a lot in different month over a year. We find that snow cover drops quickly across years in summer (June, July and August).
        In winter (Deecember, January, February), snow cover does not vary a lot across years. Explore the data by choosing the month you are interested.
    """)
    st.markdown('[Data Source: Rutgers university global snow lab](http://climate.rutgers.edu/snowcover/)')


def chart_snow_duration():
    st.title("Snow Season Length Decreases two weeks from 1972")
    st.altair_chart(vis_zyl.plot_snow_duration())
    st.write(
        """
            Snow season length is the number of days between the first snow and last snow in a year. The regression line clearly shows that the 
            season length drops quickly. Starting from 1972, it has decreased approximately two weeks, which will affect ski industry a lot.
        """
    )
    st.markdown('[Data Source: United States Environmental Protection Agency](https://www.epa.gov/)')
    

def chart_snowfall():
    st.title("Snowfall Temprorily Maintains Thanks to High Precipitation")
    st.altair_chart(vis_zyl.plot_snowfall())
    st.write("""This visualization shows that the state with higher latitude is darker which means those states experience more
              temperature increased in those areas in winter. However, most ski resorts are in high latitude states for more snowfall
              so this a bad news. In terms of snowfall, red dots dominates west which means states in the west experience obvious snowfall dropping while in other areas, 
              snow fall decreasing is not so obvious and in some place, snowfall even increases. However, this is actually misleading. 
              The snowfall increases because as temperature becomes higher, there is more evporation and leads to more precipitation. 
              Therefore, snowfall-to-precipitation ratio is a better metric.
              """)
    st.altair_chart(vis_zyl.plot_snowfall_precipitation())
    st.write("""From snowfall-to-precipitation visualization, it is clear that this ratio drops dramastically in most areas of US. Noted
    that here the size scale is different from the first figure. You can hover over above two visualizations to get the exact percentage change.""")

    st.markdown('[Data Source: United States Environmental Protection Agency](https://www.epa.gov/)')

def chart_snowfall_skiresort():
    st.title('Snowfall Conditions of Ski Resorts across North America')
    st.altair_chart(vis_cxw.plot_snowfall_skiresort())
    
    st.altair_chart(vis_cxw.plot_snowfall_scores_counts())
    st.markdown('[Data Source: zRankings](https://www.zrankings.com/ski-resorts/snow?_=1615734995765)')

def chart_ticket_price():
    st.title('Temporal Price compared with CPI and Temperature')
    st.altair_chart(vis_hhy.plot_ticket_price())

def chart_resort_snow_con():
    st.image(vis_ydm.snow_condition)

def chart_elevation():
    st.title('Snowfall and Ticket Price based on Elevation')
    tab1,tab2,tab3,tab4 = st.tabs(['All', "Higher", "Median", "Lower"])
    with tab1:
        st.image(vis_ydm.all_heights)
    with tab2:
        st.image(vis_ydm.higher_heights)
    with tab3:
        st.image(vis_ydm.median_heights)
    with tab4:
        st.image(vis_ydm.lower_heights)

visualizations = [chart_seasonal_temperature, chart_snow_cover, chart_snow_duration, chart_snowfall, chart_snowfall_skiresort, chart_ticket_price, chart_resort_snow_con, chart_elevation]
viz_options = ["Seasonal Temperature", "Snow Cover", "Snow Season Length", "Snowfall by Geography", "Snowfall at Ski Resorts", "Ticket Price","Four famous Resorts","Elevation"]

# visualizations = [chart_seasonal_temperature, chart_snow_cover, chart_snow_duration, chart_snowfall,chart_snowfall_skiresort,chart_ticket_price]
# viz_options = ["Seasonal Temperature", "Snow Cover", "Snow Season Length", "Snowfall by Geography",
#                "Snowfall at Ski Resorts in North America",
#                "Ticket Price"]

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
