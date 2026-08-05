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

if 'discharge_data' not in st.session_state or not st.session_state['discharge_data']:
    st.warning('Please Gather Site Specific Information on The Data Page')
    st.stop()


