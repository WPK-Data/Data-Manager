import streamlit as st
import numpy as np
import pandas as pd
import os
import plotly.graph_objects as go
import h5py

st.set_page_config(page_title='WPK-Data',layout='wide')

##############  specify file ###############
if 'h5_file' not in st.session_state:
    st.sidebar.error('No database selected!')
    st.error('No database selected!')
else:
    h5_file = st.session_state['h5_file']
    h5_name = st.session_state['h5_file'].name
    st.success(f'Selected database: {h5_name}')
    st.sidebar.success(f'Selected database: {h5_name}')

    st.warning('Page still under construction.')