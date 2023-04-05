import pandas as pd
import altair as alt
from vega_datasets import data
import numpy as np
import pprint

df=pd.read_csv('https://raw.githubusercontent.com/GGLeod/si649group/main/zyl/seasonal-temperature_state.csv')
snowfall=pd.read_csv('https://raw.githubusercontent.com/GGLeod/si649group/main/zyl/snowfall.csv')
snow_rain=pd.read_csv('https://raw.githubusercontent.com/GGLeod/si649group/main/zyl/snowfall_preciption.csv')
temperature=pd.read_csv('https://raw.githubusercontent.com/GGLeod/si649group/main/zyl/seasonal-temperature_US.csv')
state_map = data.us_10m.url

snowfall['Trend']=snowfall['Trend'].round(2)
df['Winter']=df['Winter'].round(2)
snow_rain['Percent_change']=snow_rain['Percent_change'].round(2)
snow_rain['Longitude']=snow_rain['Longitude'].round(2)
snow_rain['Latitude']=snow_rain['Latitude'].round(2)

state_id = {
  "AL": "01",
  "AK": "02",
  "AZ": "04",
  "AR": "05",
  "CA": "06",
  "CO": "08",
  "CT": "09",
  "DE": "10",
  "FL": "12",
  "GA": "13",
  "HI": "15",
  "ID": "16",
  "IL": "17",
  "IN": "18",
  "IA": "19",
  "KS": "20",
  "KY": "21",
  "LA": "22",
  "ME": "23",
  "MD": "24",
  "MA": "25",
  "MI": "26",
  "MN": "27",
  "MS": "28",
  "MO": "29",
  "MT": "30",
  "NE": "31",
  "NV": "32",
  "NH": "33",
  "NJ": "34",
  "NM": "35",
  "NY": "36",
  "NC": "37",
  "ND": "38",
  "OH": "39",
  "OK": "40",
  "OR": "41",
  "PA": "42",
  "RI": "44",
  "SC": "45",
  "SD": "46",
  "TN": "47",
  "TX": "48",
  "UT": "49",
  "VT": "50",
  "VA": "51",
  "WA": "53",
  "WV": "54",
  "WI": "55",
  "WY": "56"
}

name = {
    'AL': 'Alabama',
    'AK': 'Alaska',
    'AZ': 'Arizona',
    'AR': 'Arkansas',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'IA': 'Iowa',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'ME': 'Maine',
    'MD': 'Maryland',
    'MA': 'Massachusetts',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MS': 'Mississippi',
    'MO': 'Missouri',
    'MT': 'Montana',
    'NE': 'Nebraska',
    'NV': 'Nevada',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NY': 'New York',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VT': 'Vermont',
    'VA': 'Virginia',
    'WA': 'Washington',
    'WV': 'West Virginia',
    'WI': 'Wisconsin',
    'WY': 'Wyoming'
}

def addId(df):
    df['id']=len(df)*[0] 
    df['name']=len(df)*[0] 
    for k in state_id:
        df.loc[df['State']==k, 'id'] = int(state_id[k])
        df.loc[df['State']==k, 'name'] = name[k]
    return df

df = addId(df)


season='Winter'
states = alt.topo_feature(state_map, 'states')

selection1=alt.selection_single(on='mouseover');
selection2=alt.selection_single(on='mouseover');
opacity1 = alt.condition(selection1, alt.value(0.6), alt.value(0.1))
opacity2 = alt.condition(selection2, alt.value(0.8), alt.value(0.3))

map_chart = alt.Chart(states).mark_geoshape().encode(
    color=alt.Color(season+':Q', title='temperature increased (\N{DEGREE SIGN}F)', scale=alt.Scale(scheme='greys')),
    tooltip=[alt.Tooltip('name:N', title='State'), alt.Tooltip(season+':Q', title='temperature increased')],
    opacity=opacity2,
).transform_lookup(
    lookup='id',
    from_=alt.LookupData(df, key='id', fields=['name','Winter', 'Spring', 'Summer', 'Fall'])
).add_selection(selection2)


snowfall_chart = alt.Chart(snowfall).mark_circle().encode(
    latitude='Latitude:Q',
    longitude='Longitude:Q',
    size=alt.Size('adjusted:Q', title='snowfall change %', scale=alt.Scale(range=[0,1000])),
    color=alt.Color('increase:N', title="type", scale=alt.Scale(range=['red','blue'])),
    opacity=opacity1,
    tooltip=['Latitude', 'Longitude', alt.Tooltip('Trend:Q', title='Snowfall change')]
).transform_calculate(
    adjusted=alt.expr.abs(alt.datum.Trend)
).transform_calculate(
    increase='datum.Trend > 0 ? "increase" : "decrease"'
).add_selection(selection1)


A=(map_chart + snowfall_chart).resolve_scale(color='independent').configure_view(
#     fill='#C2E7FF'
)
    
chart_snowfall = A.properties(width=1000, height=800, title='Winter Temperature Change in 48 States and Snowfall Change in 419 Weather Stations')

def plot_snowfall():
    return chart_snowfall


snowfall_pre_chart = alt.Chart(snow_rain).mark_circle().encode(
    latitude='Latitude:Q',
    longitude='Longitude:Q',
    size=alt.Size('adjusted:Q', title='adjusted snowfall change %', scale=alt.Scale(range=[0,2000])),
    color=alt.Color('increase:N', title="type", scale=alt.Scale(range=['red','blue'])),
    opacity=opacity1,
    tooltip=['Latitude:Q', 'Longitude:Q', alt.Tooltip('Percent_change:Q', title='Snowfall-to-precipitation')]
).transform_calculate(
    adjusted=alt.expr.abs(alt.datum.Percent_change)
).transform_calculate(
    increase='datum.Percent_change > 0 ? "increase" : "decrease"'
).add_selection(selection1)
B=(map_chart+snowfall_pre_chart)
chart_snowfall_precipitaiton=B.properties(width=1000, height=800, title="Winter Temperature Change in 48 States and Snowfall Change in 177 Weather Stations")

def plot_snowfall_precipitation():
    return chart_snowfall_precipitaiton


from sklearn.linear_model import LinearRegression

def get_season(us_temp):
    us_temp['temperature']=us_temp['temperature'].round(2)
    def month_to_season(month):
        if 3 <= month <= 5:
            return 'Spring'
        elif 6 <= month <= 8:
            return 'Summer'
        elif 9 <= month <= 11:
            return 'Autumn'
        else:
            return 'Winter'
        
    season_colors = {
        'Winter': '#1f77b4',
        'Spring': '#2ca02c',
        'Summer': '#ff7f0e',
        'Autumn': '#d62728'
    }

    us_temp['season']=us_temp['month'].apply(month_to_season)


    seasonal_data = us_temp.groupby(['year', 'season']).agg({'temperature': 'mean'}).reset_index()

    # Define a function to fit a linear regression model and return the slope and intercept
    def fit_linear_regression(x, y):
        model = LinearRegression()
        model.fit(x, y)
        slope = model.coef_[0]
        intercept = model.intercept_
        return slope, intercept

    # Calculate the slope and intercept for each season
    seasons = ['Winter', 'Spring', 'Summer', 'Autumn']
    regression_params = {}

    for season in seasons:
        season_data = seasonal_data[seasonal_data['season'] == season]
        x = season_data[['year']]
        y = season_data['temperature']
        slope, intercept = fit_linear_regression(x, y)
        regression_params[season] = (slope, intercept)
        
        
    # Define a function to format the regression formula as a string
    def format_regression_formula(slope, intercept):
        return f"y = {slope:.3f}x + {intercept:.2f}"

    # Create text annotations for each season
    text_annotations = []

    for i, season in enumerate(seasons):
        slope, intercept = regression_params[season]
        formula = format_regression_formula(slope, intercept)
        annotation = alt.Chart({'values': [{'x': 1905, 'y': 80 - i * 5, 'text': f"{season}: {formula}"}]}).mark_text(
            fontSize=12,
            align='left',
            baseline='middle',
            dx=5
        ).encode(
            x='x:Q',
            y='y:Q',
            text='text:N'
        )
        text_annotations.append(annotation)
        
    def apply_regression(year, season):
        slope, intercept = regression_params[season]
        return year * slope + intercept

    seasonal_data['Regression'] = seasonal_data.apply(lambda row: apply_regression(row['year'], row['season']), axis=1)
    annotation_data = []

    for season in seasons:
        slope, intercept = regression_params[season]
        formula = format_regression_formula(slope, intercept)
        x_position = 2023  # Adjust this value to control the position of the annotation along the x-axis
        y_position = apply_regression(x_position, season)
        annotation_data.append({'season': season, 'year': x_position, 'temperature': y_position, 'text': formula})

    annotation_df = pd.DataFrame(annotation_data)

    text_marks = alt.Chart(annotation_df).mark_text(
        fontSize=12,
        align='left',
        baseline='middle',
        dx=5
    ).encode(
        x=alt.X('year:Q', title='Year'),
        y=alt.Y('temperature:Q', title='Temperature (\N{DEGREE SIGN}F)'),
        text='text:N',
        color=alt.Color('season:N', title='Season')
    )

    base = alt.Chart(seasonal_data).mark_line().encode(
        x=alt.X('year:Q', title='Year',scale=alt.Scale(domain=[1890, 2050])),
        y=alt.Y('temperature:Q', scale=alt.Scale(domain=[25, 80])),
        color=alt.Color('season:N', scale=alt.Scale(domain=list(season_colors.keys()), range=list(season_colors.values()))),
        tooltip=[alt.Tooltip('year:Q'), alt.Tooltip('season:N'), alt.Tooltip('temperature:Q')]
    ).properties(
        width=800,
        height=400,
        title='Seasonal Temperature from 1895 to 2023'
    )

    # Create the regression line chart
    regression = base.transform_regression(
        on='year',  # Independent variable
        regression='temperature',  # Dependent variable
        groupby=['season']  # Group by season
    ).mark_line(strokeDash=[4, 4])  # Dashed line style for the regression line


    nearest = alt.selection(type='single', nearest=True, on='mouseover', fields=['year'], empty='none')
    points = base.mark_circle().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    ).add_selection(
        nearest
    )

    rules = alt.Chart(seasonal_data).mark_rule(color='gray').encode(
        x='year:Q'
    ).transform_filter(
        nearest
    )

    text = base.mark_text(align='left', dx=5, dy=-5).encode(
        text=alt.condition(nearest, alt.Text('temperature:Q', format='.2f'), alt.value(' '))
    ).transform_filter(
        nearest
    )

    # year_text = base.mark_text(align='left', dx=5, dy=10).encode(
    #     text=alt.condition(nearest, 'year:Q', alt.value(' '))
    # ).transform_filter(
    #     nearest
    # )


    # combined_chart.display()
    final_chart = alt.layer(base, regression, points, rules, text, text_marks).properties(
        width=800,
        height=400,
        title='Seasonal Temperature from 1895 to 2023 with Linear Regression in US'
    )

    return final_chart

def plot_seasonal_temperature():
    df=pd.read_csv("https://raw.githubusercontent.com/GGLeod/si649group/main/zyl/US_temperature.csv")
    # return get_season(df)
    return get_season(df).interactive()

duration=pd.read_csv('https://raw.githubusercontent.com/GGLeod/si649group/main/zyl/snow_duration.csv')

base2=alt.Chart(duration).mark_line().encode(
    x='Year:Q',
    y=alt.Y('Duration:Q', title='Snow Season Length in US', scale=alt.Scale(domain=[100, 180]))
)

regression2 = base2.transform_regression(
    on='Year',  # Independent variable
    regression='Duration',  # Dependent variable
).mark_line(strokeDash=[4, 4])  # Dashed line style for the regression line


def plot_snow_duration():
    return (base2+regression2).interactive().properties(
        width=800,
        height=400,
        title='Snow Season Length from 1972-2013 in US'
    )

coverage=pd.read_csv('https://raw.githubusercontent.com/GGLeod/si649group/main/zyl/snow_cover.csv')

coverage['coverage']=coverage['coverage']/1000000.0

base3=alt.Chart(coverage).mark_line().encode(
    x='year',
    y=alt.Y('mean(coverage)', title='snow cover (million sq. km)'),
)

regression3 = base3.transform_regression(
    on='year',  # Independent variable
    regression='coverage',  # Dependent variable
).mark_line(strokeDash=[4, 4])  # Dashed line style for the regression line



month=list(coverage['month'].unique())
month.sort()

selectOrigin=alt.selection_single(
    fields=['month'], # our selection is going to select based on origin
    init={"month":month[0]}, # what should the start value be?
    
    # now creat a binding (binding_select is a drop down)
    bind=alt.binding_select(options=month,name="Select Month "),
    #"options" is required, "name" within here will override.
)


base4=alt.Chart(coverage).mark_line().encode(
    x='year',
    y=alt.Y('coverage', title='snow cover (million sq. km)'),
    color=alt.value('red')
#     opacity=filter_opacity
).transform_filter(
    selectOrigin
).add_selection(
    selectOrigin
)


mid_x = coverage['year'].mean()
max_y = coverage['coverage'].mean()
# Text annotation
text_annotation = alt.Chart(pd.DataFrame({
    'x': [mid_x],
    'y': [max_y],
    'text': ['year average']
})).mark_text(dy=-10).encode(
    x=alt.X('x', title="year"),
    y='y',
    text='text'
)

# base3+regression3
def plot_snow_cover():
    return (base4+base3+regression3+text_annotation).interactive().properties(
        width=800,
        height=400,
        title='Snow Cover in Different Months in North America'
    )

