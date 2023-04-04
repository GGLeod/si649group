import streamlit as st

import zyl.visualize as vis_zyl

st.title("How Can Global Warming Impact Ski Industry")

st.altair_chart(vis_zyl.plot_seasonal_temperature(), use_container_width=True)
st.altair_chart(vis_zyl.plot_snow_cover(), use_container_width=True)
st.altair_chart(vis_zyl.plot_snow_duration(), use_container_width=True)
st.altair_chart(vis_zyl.plot_snowfall, use_container_width=True)
st.altair_chart(vis_zyl.plot_snowfall_precipitation, use_container_width=True)

