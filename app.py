import streamlit as st
import os
import pandas as pd
import requests
import folium
import geopandas
import mapclassify
from dataretrieval import waterdata
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

st.title("Simplified USGS Discharge Portal :)")

if 'usgs_key' not in st.session_state:
    st.session_state['usgs_key'] = None

def validate_key(api_key):
    os.environ['API_USGS_PAT'] = api_key
    try:
        test, _ = waterdata.get_reference_table("parameter-codes")
        return len(test) > 0
    except Exception:
        return False

if not st.session_state['usgs_key']:
    st.info("Please enter your API key below before proceeding")
    user_key = st.text_input("API Key", type="password")
    st.link_button("Get your USGS API Key Here", "https://api.waterdata.usgs.gov/signup/")

    if st.button("Submit"):
        if validate_key(user_key):
            st.session_state['usgs_key'] = user_key
            st.success("API key validated!")
            st.rerun()
        else:
            st.error("Invalid API key — please Double Check your Key")
else:
    # rest of your app goes here
    st.success("API key set — ready to go!")
    st.write("Please Proceed to the Data page on the sidebar.")
    
    

  

  
