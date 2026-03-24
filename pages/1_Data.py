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
    st.stop()

else:
  os.environ['API_USGS_PAT'] = st.session_state['usgs_key']

state = st.text_input("Ex New Mexico")
st.session_state['us_state'] = state:

if st.session_state['us_state'] != None:

try:
   NM_discharge, _ = waterdata.get_time_series_metadata(
       state_name=state,
       parameter_code="00060",
       skip_geometry=True,
     )
   if len(NM_discharge) == 0:
      st.warning(f'You have Selected {state}, there are no records for this entry.')
   if len(NM_discharge > 0:
      st.info(f'You have selected {state}')

except:
   st.warning("Something Went Wrong")
   
