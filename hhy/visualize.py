import requests
import pandas as pd
from bs4 import BeautifulSoup
import warnings
warnings.simplefilter("ignore")
import altair as alt
from vega_datasets import data

price_df = pd.read_csv('hhy/dataset/price.csv', sep = '\t')
cpi_df = pd.read_csv('hhy/dataset/cpi.csv', sep = '\t')

cpi_chart = alt.Chart(cpi_df).mark_line(point=True).encode(
    x=alt.X('Year:O',axis=alt.Axis(labelAngle=-45)),
    y=alt.Y('Avg:Q',title='CPI'),
    color=alt.value("#FFAA00")
)
states_url = data.us_10m.url
state_id = data.population_engineers_hurricanes()[['state','id']]
states = alt.topo_feature(data.us_10m.url, feature = 'states')

temp_df = pd.read_csv('hhy/dataset/climdiv_state_year.csv')
temp_df =temp_df.rename(columns={'fips':'id'})
temp_new_df = temp_df[(temp_df.year >= 1994)]
selection_state=alt.selection_single(fields=['id'], init={"id":9})
colorCondition = alt.condition(selection_state,alt.value(1.0), alt.value(0.1))
year_slider = alt.binding_range(min=1994, max=2022, step=1, name="Year")
slider_selection = alt.selection_single(bind=year_slider, fields=['Year'])
price_state_df = pd.merge(price_df,state_id,left_on='state', right_on='state',how='left')
price_state_mean_df = price_state_df.groupby(['state','Year','id']).agg(
    {'price': 'mean'}
).reset_index()
scale = alt.Scale(
    domain=[20, 120],
    type='linear'
)
background = alt.Chart(price_state_mean_df).transform_lookup(
    lookup='id',
    from_=alt.LookupData(states,'id',fields=['geometry','type'])
).mark_geoshape(
    stroke='black', strokeWidth=1,
).encode(
    color=alt.Color('price', scale=scale)
).add_selection(
    slider_selection,selection_state
).transform_filter(
    slider_selection
).project(
    type='albersUsa'
).properties(
    width = 600,
    height= 500
)
price_selection = alt.Chart(price_state_df).transform_lookup(
    lookup='id',
    from_=alt.LookupData(states,'id',fields=['geometry','type'])
).transform_filter(
    selection_state
).mark_line(point=True).encode(
    x=alt.X('Year:O',axis=alt.Axis(labelAngle=-45),title=None),
    y=alt.Y('mean(price):Q',title='Ticket Price ($)'),
)
temp_selection = alt.Chart(temp_new_df).transform_lookup(
    lookup='id',
    from_=alt.LookupData(states,'id',fields=['geometry','type'])
).transform_filter(
    selection_state
).mark_line(point=True).encode(
    x=alt.X('year:O',axis=alt.Axis(labelAngle=-45),title=None),
    y=alt.Y('temp:Q',title='Temperature (℉)',scale=alt.Scale(domain=[40, 55])),
    color=alt.value("#FFAA00")
)
price_cpi_chart = (price_selection + cpi_chart ).resolve_scale(
    y='independent'
).properties(
    title=alt.TitleParams(text='Tickect Price vs. CPI', fontSize=12),
    width = 300,
    height = 200
)
price_temp_chart = (price_selection + temp_selection).resolve_scale(
    y='independent',
).properties(
    title=alt.TitleParams(text='Tickect Price vs. Temperature', fontSize=12),
    width = 300,
    height= 200
)
price_change_chart = (background | (price_cpi_chart & price_temp_chart)).configure_title(fontSize=30).properties(
        title = 'Ticket Price From 1994-2022'
    )

def plot_ticket_price():
    return price_change_chart