import streamlit as st
import os
import pandas as pd
import requests
from dataretrieval import waterdata
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

st.title("Discharge Data")

if 'us_state' not in st.session_state:
  st.session_state['us_state'] = None

if 'usgs_key' not in st.session_state:
    st.session_state['usgs_key'] = None
    st.warning('Please Enter Your API Key on the APP Page')

else:
  os.environ['API_USGS_PAT'] = st.session_state['usgs_key']

state = st.text_input("Ex New Mexico")
try:
  NM_discharge, _ = waterdata.get_time_series_metadata(
    state_name=state,
    parameter_code="00060",
    skip_geometry=True,
  )
  st.sucess(f'You have Selected{state}')
except:
  st.warning("Try entering the state again")
