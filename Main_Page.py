import streamlit as st
import numpy as np
import pandas as pd
import os

import plotly.graph_objects as go
import h5py
import matplotlib.pyplot as plt


#from streamlit_option_menu import option_menu
# ############## ---------------------- ###############
# window = option_menu(
#     menu_title = 'WPK Data Manager',
#     options = ['Entry','Treatment','Visualization'],
#     icons = ['pencil-fill','calculator-fill','bar-chart-fill'],
#     orientation = 'horizontal')
# #if window == 'Entry': #+ indentation

st.set_page_config(page_title='WPK-Data',layout='wide')
#''' General settings '''
#st.title('hello there')

# hide_st_style = '''
#             <style>
#             #MainMenu {visibility: hidden;}
#             footer {visibility: hidden;}
#             header {visibility: hidden;}
#             <\style>
#             '''
#st.markdown(hide_st_style, unsafe_allow_html = True)


##############  specify file ###############
col26, col27 = st.columns([5,5])

with col26.expander('Database selection'):
    h5_file = st.file_uploader('Choose HDF5-File',accept_multiple_files = False,type = ['h5','hdf5'])
    if h5_file:
        with h5py.File(h5_file, 'a') as f:
            new_L0 = list(f.keys())
            st.session_state.layer0 = new_L0
            st.session_state.layer0.append('-')
        
with col27.expander('Create New'):
    with st.form('new_hdf5',clear_on_submit=True):
        st.text_input('Name of database',value='st_h5_try',key='h5_name',placeholder='File name')
        st.text_input('File location',value=r'G:\My Drive\Data_HDF5\app_streamlit',key='h5_path',placeholder='File path')
        st.text_input('Researcher',value='JohWie',key='h5_researcher',placeholder='Who works on this project?')
        st.text_input('Project',value='digi',key='h5_proj',placeholder='Which project or PhD-thesis is this work part of?')
        st.text_input('Materials',value='PP, GFK, CFK',key='h5_mats',placeholder='What types of materials were investigated?')
        st.text_input('Timeframe',value='2023',key='h5_date',placeholder='When was this work done?')
        make_h5 = st.form_submit_button('Create hdf5')   

             
        if make_h5:        
            if '.hdf5' not in st.session_state.h5_name and '.h5' not in st.session_state.h5_name:
                name_corr = st.session_state.h5_name+'.hdf5'
                new_h5_file = os.path.join(st.session_state.h5_path, name_corr)
            else:
                new_h5_file = os.path.join(st.sessions_state.h5_path, st.session_state.h5_name)
            st.write(new_h5_file)
            with h5py.File(new_h5_file, 'a') as f:
                proj = f.require_group(st.session_state.h5_proj)
                proj.attrs['Researcher'] = st.session_state.h5_researcher
                proj.attrs['Materials'] = st.session_state.h5_mats
                proj.attrs['Timeframe'] = st.session_state.h5_date

if h5_file:
    st.session_state['h5_file'] = h5_file

#''' ------------------------------- '''

if 'h5_file' not in st.session_state:
    st.sidebar.error('No database selected!')
    st.error('No database selected!')
else:
    h5_name = st.session_state['h5_file'].name
    st.success(f'Selected database: {h5_name}')
    st.sidebar.success(f'Selected database: {h5_name}')
#''' ------------------------------- '''

st.session_state['upl_rdy'] = False



