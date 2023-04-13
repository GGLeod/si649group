import streamlit as st
import pandas as pd

import zyl.visualize as vis_zyl
import cxw.visualize as vis_cxw
import hhy.visualize as vis_hhy
# import ydm.visualize as vis_ydm

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
         We find that snow cover drops quickly across years in summer (June, July and August).
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
    st.title("Snowfall Drops Most in North-West but Overall Temprorily Maintains Thanks to High Precipitation")
    st.altair_chart(vis_zyl.plot_snowfall())
    st.write("""This visualization shows that the state with higher latitude is darker which means those states experience more
              temperature increased in those areas in winter. However, most ski resorts are in high latitude states for more snowfall
              so this a bad news. In terms of snowfall, red dots dominates north-west which means states in the north-west experience obvious snowfall dropping while in other areas, 
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
    st.write(""" This visualization shows the snow amount and snowfall score of different ski resort across North America (tooltip shows the exact number). Skiing is not 
    only about snow quantity, quality also matters. Snowfall score is a rating accounting for snowfall quantity, quality and consistency. 
    It’s a good indicator of the attractiveness of a resort for powder skiing.""")
    st.write("""We can tell the ski resort with high snowfall score is mostly in the north-west of US. However, from previous visualizations, 
    we know snowfall drops most in the north-west, this is an alert to ski industry. You can interact with following graph to see the number of resorts within a snowfall score range.
    Resorts with high snowfall score are too precious to be ruined.""")
    st.altair_chart(vis_cxw.plot_snowfall_scores_counts())
    st.markdown('[Data Source: zRankings](https://www.zrankings.com/ski-resorts/snow?_=1615734995765)')

def chart_ticket_price():
    st.title("Ticket Price is Increasing Faster than CPI")
    st.altair_chart(vis_hhy.plot_ticket_price(), use_container_width=True)
    st.write("""This visualization shows the ticket price of ski resort in New England. You can drag the slider to see the increasing of the ticket price.
    Of course, the ticket price increasing is not all about climate. Therefore, we compare it with CPI (the price of a weighted average market basket of 
    consumer goods and services purchased by households). By clicking a state, you can see the ticket price vs 
    CPI of that state. We can see it is obvious that the ticket price increases much faster than CPI. One reason is that the increasing cost to maintain snow 
    condition such as snow making. """)
    st.markdown('[Data Source: New England Ski History](https://www.newenglandskihistory.com/timeline/)')
    st.markdown('[Data Source: U.S. BUREAU OF LABOR STATISTICS](https://www.bls.gov/regions/new-england/data/consumerpriceindex_northeast_table.htm)')


def snow_vs_price():
    st.title("The Corelation between Ticket Price and Snow Amount by Mountain Height")
    st.write("For the following visualizations, we eliminated the effect of price levels in different states by diving the price by the state's cost of living index.")
    low = "Low 0~450m"
    median = "Median 450~900m"
    high = "High > 900m"
    tabs = ['All', low, median, high]
    selected_tab = st.selectbox("Mountain Height", tabs)
    if selected_tab == 'All':
        st.image("YDM/ALL.png")
    elif selected_tab == low:
        st.image("YDM/LOWER.png")
    elif selected_tab == median:
        st.image("YDM/MEDIAN.png")
    elif selected_tab == high:
        st.image("YDM/HIGHER.png")
    
    st.write(""" Ticket price of a ski resort is related to many factors besides snow condition. One of the most important factors is height. A ski resort on a higher mountain typically has higher operation cost and favored by skiers. By choosing the height of mountains above, we can find the ticket price of ski resorts is highly related to the mountain height.

The interesting finding is that, the correlation between snow amount and price is negative relationship in median height mountain and the correlation is positive for higher mountain. There is probability many reasons and factors lead to this interesting opposite correlation. One factor we consider is **Artificial Snow Making** and **Customers Segments**. 

For snow making, the median height resort may have good snow making equipment, so when the snow condition is poor, they will be making snow with higher cost, which lead to higher ticket price; and if the snow amount is high, the cost of snow making is lower with lower price, which could attract more customers. The customers of lower height mountain resort are almost locally, and the snow making cost is too high to using, so when the snow condition is good, the resort will increasing the price and making more profit from the snow condition and customers.""")

    st.write(""" To see this point more clearly. Below is the visualization of the snowcondition of four resorts. A bluebird day is a day
      with clear skies, bright sunshine, and no clouds, resulting in excellent visibility and beautiful views on the mountain. A powder day is 
      a day when a significant amount of fresh snow has fallen, creating a layer of light, fluffy, and deep snow known as "powder."
    We can see that height dominates the ticket price overall. Alpental and KeyStone are much more expensive than other two regardless of the snow condition. """)

    data = {
        "Resort Name": ['Alpental', 'Arizona', 'KeyStone', 'Mt Holly'],
        "Height(m)": [957, 576, 953, 106],
        "Price($)": [128, 49, 179, 55]
    }

    df = pd.DataFrame(data)

    st.write(df)

    st.image("YDM/snow_4_resorts.png")

    st.markdown('[Data Source: Economic Research and Information Center](https://meric.mo.gov/data/cost-living-data-series)')
    st.markdown('[Data Source: On the Snow](https://www.onthesnow.com/)')


    

    # tab1, tab2, tab3, tab4 = st.tabs(['All','Low','Median','High'])
    # with tab1:
    #     st.image("YDM/ALL.png")
    # with tab2:
    #     st.image("YDM/LOWER.PNG")
    # with tab3:
    #     st.image("YDM/MEDIAN.PNG")
    # with tab4:
    #     st.image("YDM/HIGH.PNG")
    


visualizations = [chart_seasonal_temperature, chart_snow_cover, chart_snow_duration,
                   chart_snowfall, chart_snowfall_skiresort, chart_ticket_price, snow_vs_price]
viz_options = ["Seasonal Temperature", "Snow Cover", "Snow Season Length", 
               "Climate Change by Geography", "Snowfall by Geography", "Ticket Price vs CPI", "Ticket Price vs Snowfall Condition"]

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
