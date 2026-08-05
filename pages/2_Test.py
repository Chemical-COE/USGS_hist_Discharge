import streamlit.components.v1 as components
import streamlit as st
import os
import pandas as pd
import requests
import plotly.express as px
from dataretrieval import waterdata
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
import geopandas as gpd

st.title("Simplified USGS Discharge Portal :)")

if 'usgs_key' not in st.session_state or not st.session_state['usgs_key']:
    st.warning('Please Enter Your API Key on the App Page')
    st.stop()

if 'discharge_data' not in st.session_state:
    st.warning('Please Gather Site Specific Information on The Data Page')
    st.stop()

discharge_data = st.session_state['discharge_data']

st.info('Use the inputs below to select the time frame you are interested in.')
st.write('Make sure to use the format yyyy-mm-dd')

start_date = st.text_input("Start Date", "2020-01-01")
st.write("The current start date is:", start_date)

end_date = st.text_input("End Date", "2023-01-01")
st.write("The current end date is:", end_date)


filtered_df = discharge_data[discharge_data['time'].between(start_date, end_date)].copy()
st.dataframe(filtered_df)

st.info('Select the gages you would like to make a hydrograph.')
st.write('You can manually turn on and of any gage by selecting it in the legend to the right.')
st.write('You can Double click the Legend on the right to clear all the gages.')

# df Columns
# Index(['time_series_id', 'monitoring_location_id', 'parameter_code',
#       'statistic_id', 'time', 'value', 'unit_of_measure', 'approval_status',
#       'qualifier', 'last_modified', 'daily_id'],
#      dtype='object')

fig = px.scatter(
    filtered_df, # Point to our Data
    x='time', # Define Our Longitudinal Axis
    y='value',
    color='monitoring_location_id',
    hover_data=['monitoring_location_id', 'time' , 'unit_of_measure', 'approval_status'], # Write out what we want in oir label.
    title='River Hydrograph', # Add A Title. :D
    #markers=True
)
st.plotly_chart(fig)

fig_log = px.scatter(
    filtered_df, # Point to our Data
    x='time', # Define Our Longitudinal Axis
    y='value',
    color='monitoring_location_id',
    hover_data=['monitoring_location_id', 'time' , 'unit_of_measure', 'approval_status'], # Write out what we want in oir label.
    title='River Hydrograph Log Scaled', # Add A Title. :D
    #markers=True
)

fig_log.update_layout(yaxis_type="log")
st.plotly_chart(fig_log)


