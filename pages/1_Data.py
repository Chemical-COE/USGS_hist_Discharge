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
if 'search_data' not in st.session_state:
    st.session_state['search_data'] = None
if 'NM_locations_discharge' not in st.session_state:
    st.session_state['NM_locations_discharge'] = None
if 'NM_search' not in st.session_state:
    st.session_state['NM_search'] = None
if 'run_button' not in st.session_state:
    st.session_state['run_button'] = None

if 'usgs_key' not in st.session_state or not st.session_state['usgs_key']:
    st.warning('Please Enter Your API Key on the App Page')
    st.stop()
else:
    os.environ['API_USGS_PAT'] = st.session_state['usgs_key']

state = st.text_input("Enter a US State (Ex: New Mexico)")
st.session_state['us_state'] = state

if st.session_state['us_state']:
    try:
        NM_discharge, _ = waterdata.get_time_series_metadata(
            state_name=state,
            parameter_code="00060",
            skip_geometry=True,
        )

        if len(NM_discharge) == 0:
            st.warning(f"No records found for '{state}' — check spelling")
            st.stop()

        st.info("This step can take a while. Wait for the program to tell you to proceed.")

        NM_locations, _ = waterdata.get_monitoring_locations(
            state_name=state,
            site_type_code="ST",
            skip_geometry=True,
        )

        NM_locations_discharge = NM_locations.loc[
            NM_locations["monitoring_location_id"].isin(
                NM_discharge["monitoring_location_id"].unique().tolist()
            )
        ]

        st.session_state['NM_locations_discharge'] = NM_locations_discharge
        st.session_state['NM_search'] = 'ready'
        st.success(f"Found {len(NM_locations_discharge)} stream sites in {state}. You can proceed.")

    except Exception as e:
        st.warning(f"Something went wrong — check your state name. Error: {e}")
        st.stop()

if st.session_state['NM_search'] == 'ready':
    st.write('Try to Refine Your Search')
    region = st.text_input("Enter a refining search (Ex: Pecos)")
    
    if st.button('Run Analysis'):
        st.session_state['run_button'] = 'RUN'
    
    if st.session_state['run_button'] != 'RUN':
        st.stop()
    
    region_submit = str.upper(region)
    
    region_sites = NM_locations_discharge.loc[
    NM_locations_discharge["monitoring_location_name"].str.contains(region_submit, case=False)
    ]

    region_ids = region_sites["monitoring_location_id"].tolist()
    if len(region_ids) > 0:
        o = 1
    
    else:   
        o = 0

    if l + o == 2:
        st.info(f"We found {region} {len(region_ids)} sites they are bellow")
        st.dataframe(region_ids)
        st.info('The next step can take a few moments to load')

        df_region, _ = waterdata.get_daily(
        monitoring_location_id=region_ids,
        parameter_code="00060",
        statistic_id="00003",
        time="1910-01-01/..",
        skip_geometry=True,
        )
        
        st.info(f'We found {len(df_region)} "daily" dioscharge measurments in {region}')
        st.dataframe(df_region)

        st.download_button(
            label="Download Daily Data",
            data=df_region.to_csv(index=False),
            file_name="discharge_locations.csv",
            mime="text/csv"
            )
        
    
