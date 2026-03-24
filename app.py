import streamlit as st
import os
import pandas as pd
import requests
from dataretrieval import waterdata
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

if 'usgs_key' not in st.session_state:
    st.session_state['usgs_key'] = 'no_key'

if st.session_state['usgs_key'] == 'no_key':
  st.info("Please Enter your API Key below before Proceeding")
  user_input = st.text_input("Please Type Here")
  st.link_button("Get your USGS API Key Here", "https://api.waterdata.usgs.gov/signup/")
  

  
