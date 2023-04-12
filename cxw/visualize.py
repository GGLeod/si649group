import pandas as pd
import altair as alt
from vega_datasets import data

df = pd.read_csv("cxw/zRankings.csv")
state_map = data.us_10m.url
states = alt.topo_feature(state_map, feature='states')
us = alt.Chart(states).mark_geoshape(
    fill = '#f6f4e9',
    stroke='black',
    strokeWidth=0.5
).properties(
    width=1000,
    height=800
).project(
    "albersUsa"
    ) 
points = alt.Chart(df).mark_circle(opacity=0.9, stroke = 'white').encode(
    latitude='latitude:Q',
    longitude='longitude:Q',
    size=alt.Size('True Snow Per Year (inches):Q', scale=alt.Scale(range=[0,660]), legend = alt.Legend(title = 'True Snow Per Year (inches)')),
    color=alt.Color('Snowfall Score:Q', scale=alt.Scale(domain=[30, 50, 70, 90], scheme='blueorange'), legend=alt.Legend(title='Snowfall Score')),
    tooltip = [
        alt.Tooltip('Resort Name', title='Resort Name'),
        alt.Tooltip('State_full', title='Location'),
        alt.Tooltip('True Snow Per Year (inches):Q', title='Snow Per Year (inches)'),
        alt.Tooltip('MonthsMoreThan90Snow', title='Extended Stay'),
        alt.Tooltip('MonthsLessThan30Snow:Q', title='Drought Threat')
        ])
# import geopandas as gpd
# fp = gpd.datasets.get_path('naturalearth_lowres')
# gdf_ne = gpd.read_file(fp)
# gdf_sel = gdf_ne[gdf_ne.continent == 'North America']
# gdf_sel['geometry'] = gdf_sel['geometry'].apply(lambda x: x.__geo_interface__)

chart = alt.layer(
    us, points)

title = alt.TitleParams(
    'Snowfall at Ski Resorts in North America',
    subtitle='Data source: ZRankings',
    subtitleColor='#555',
    dy=-20,
    fontSize=20
)
snowfall_at_ski_resort_in_north_america = chart.configure_title(
    fontSize=24,
    anchor='middle',
    color='#333'
).configure_legend(
    labelFontSize=12,
    titleFontSize=12,
    padding=30
).configure_view(
    strokeWidth=0
).properties(
    title=title,
    width=800,
    height=500
)

def plot_snowfall_skiresort():
    return snowfall_at_ski_resort_in_north_america


brush = alt.selection_interval(encodings=['x'])
histogram = alt.Chart(df).mark_bar().encode(
    x=alt.X('Snowfall Score:Q', bin=alt.Bin(step=10), axis=alt.Axis(title='Snowfall Score')),
    y=alt.Y('count()', axis=alt.Axis(title='Number of Resorts')),
    color=alt.condition(brush, alt.value('#e39e19'), alt.value('lightgray'))
).properties(
    width=700,
    height=150
).add_selection(
    brush
)
resort_count = alt.Chart(df).transform_filter(
    brush
).mark_text(
    fontSize=48,
    fontWeight=600,
    color='#e39e19'
).encode(
    text='count()'
)
snowfall_scores_counts = (histogram & resort_count)
def plot_snowfall_scores_counts():
    return snowfall_scores_counts


























