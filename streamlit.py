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
    st.title("Ticket Price is increasing faster than CPI")
    st.altair_chart(vis_hhy.plot_ticket_price(), use_container_width=True)
    st.write("""This visualization shows the ticket price of ski resort in New England. You can drag the slider to see the increasing of the ticket price.
    Of course, the ticket price increasing is not all about climate. Therefore, we compare it with CPI (the price of a weighted average market basket of 
    consumer goods and services purchased by households). By clicking a state, you can see the ticket price vs 
    CPI of that state. We can see it is obvious that the ticket price increases much faster than CPI. One reason is that the increasing cost to maintain snow 
    condition such as snow making. """)

visualizations = [chart_seasonal_temperature, chart_snow_cover, chart_snow_duration, chart_snowfall, chart_snowfall_skiresort, chart_ticket_price]
viz_options = ["Seasonal Temperature", "Snow Cover", "Snow Season Length", "Snowfall by Geography", "Snowfall at Ski Resorts", "Ticket Price"]

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
