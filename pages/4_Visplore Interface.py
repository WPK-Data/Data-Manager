import streamlit as st
import numpy as np
import pandas as pd
import os
import plotly.graph_objects as go
import h5py

st.set_page_config(page_title='WPK-Data',layout='wide')

def storename(name,all_paths):
  all_paths.append(name)
  
def path_finder(h5_file, filter_list): 
  all_paths = []
  filtered_paths = [] 

  with h5py.File(h5_file, 'r') as f:    
    # Call the visit() function to recursively visit each node in the file
    #then use the storename-function to store the name in the list of paths
    f.visit(lambda name: storename(name,all_paths))
    
    print('All available paths:')
    for a_p in all_paths:
      print(a_p)
      #check, which nodes have the right names and are actual datasets
      check_name = all([filter.lower() in a_p.lower() for filter in filter_list])
      check_type = isinstance(f.get(a_p),h5py.Dataset)
      if check_name and check_type:
          filtered_paths.append(a_p)
    print('\n')

  if len(filtered_paths) == 0:
    print('No valid path to satisfy all filters.')
  else:
    print('List of filtered paths:')
    for p in filtered_paths:
      print(p)
    print('\n')
  return filtered_paths

def generate_row_name(strings):
  row_name = ''
  for string in strings:
    if string != '' and len(row_name) == 0:
       row_name = string
    elif string != '' and len(row_name)>0:
      row_name = row_name + '_' + string
  return row_name

def generate_new_row(row_name,h5_name,selected_sets,attributes,arrays,decomp_x,decomp_y,custom_inputs):
  df = pd.DataFrame()
  df['Material name'] = [row_name]

  with h5py.File(h5_name, 'r') as f:
      for set in selected_sets:
        for arr in arrays:
          if arr in f[set].dtype.names:
            arr_ay = [f[set][arr]]          
            df[arr] = arr_ay
          
        for attr in attributes:
          if attr in f[set].attrs.keys():
            df[attr] = f[set].attrs[attr]

        df = add_decompositions(df,row_name,f[set],decomp_x,decomp_y)

  for k,v in custom_inputs.items():
    df[k] = v

  return df

def add_decompositions(df,row_name,set,decomp_x,decomp_y):
  for x_name,y_name in zip(decomp_x,decomp_y):
    if x_name in set.dtype.names and y_name in set.dtype.names:
      for x_val, y_val in zip(set[x_name],set[y_name]):
        col_name = f'{x_name} = {x_val}'
        df[col_name] = y_val

  return df
##############  specify file ###############

if 'h5_file' not in st.session_state:
    st.sidebar.error('No database selected!')
    st.error('No database selected!')
else:
    h5_file = st.session_state['h5_file']
    h5_name = st.session_state['h5_file'].name
    st.success(f'Selected database: {h5_name}')
    st.sidebar.success(f'Selected database: {h5_name}')
    '''---'''
    st.subheader('Select up to 4 keywords to narrow down dataset selection!')
    keycol1, keycol2, keycol3, keycol4 = st.columns((3,3,3,3))
    keycol1.text_input('Keyword 1:', value = '', key ='key1')
    keycol2.text_input('Keyword 2:', value = '', key ='key2')
    keycol3.text_input('Keyword 3:', value = '', key ='key3')
    keycol4.text_input('Keyword 4:', value = '', key ='key4')

    filter_list = [st.session_state['key1'],st.session_state['key2'],st.session_state['key3'],st.session_state['key4']]
    paths = path_finder(h5_name,filter_list)
    
    selected_sets = []
    line_data = []
    point_data = []
    for p in paths:
        st.checkbox(p,value=True,key=p)
        with h5py.File(h5_name, 'r') as f:
            st.write(f.attrs.keys())   
            if st.session_state[p]:
                selected_sets.append(p)
                try:
                    for col_name in f[p].dtype.names:
                        if col_name not in line_data:
                            line_data.append(col_name)
                except:
                   st.warning('Some datasets had no valid line data.')
                try:
                    for attr_name in f[p].attrs.keys():                                             
                        if attr_name not in point_data:
                            point_data.append(attr_name)
                except:
                   st.warning('Some datasets had no valid point data.')

    df_col1, df_col2, df_col3, df_col4 = st.columns((3,3,3,3))


    df_col1.text_input('Custom input 1 (text)', value = '', key ='custom parameter 1', placeholder='enter text')
    df_col2.text_input('Custom input 2 (text)', value = '', key ='custom parameter 2', placeholder='enter text')
    df_col3.text_input('Custom input 3 (text)', value = '', key ='custom parameter 3', placeholder='enter text')
    df_col4.text_input('Custom input 4 (text)', value = '', key ='custom parameter 4', placeholder='enter text')
    df_col1.number_input('Custom input 5 (number)', key ='custom parameter 5')
    df_col2.number_input('Custom input 6 (number)', key ='custom parameter 6')
    df_col3.number_input('Custom input 7 (number)', key ='custom parameter 7')
    df_col4.number_input('Custom input 8 (number)', key ='custom parameter 8')
    df_col1.number_input('Custom input 9 (number)', key ='custom parameter 9')
    df_col2.number_input('Custom input 10 (number)', key ='custom parameter 10')
    df_col3.number_input('Custom input 11 (number)', key ='custom parameter 11')
    df_col4.number_input('Custom input 12 (number)', key ='custom parameter 12')
    
    df_col1.multiselect('Single Point Data', point_data, key ='single_data')
    df_col2.multiselect('Multipoint Data (array)', line_data, key ='multi_data_array')
    df_col3.multiselect('Multipoint Data (decomposition X-value)', line_data, key ='multi_data_decompose_x_val')
    df_col4.multiselect('Multipoint Data (decomposition Y-values)', line_data, key ='multi_data_decompose_y_val')
    '''---'''

    custom_keys = ['custom parameter 1','custom parameter 2','custom parameter 3','custom parameter 4',\
                   'custom parameter 5','custom parameter 6','custom parameter 7','custom parameter 8',\
                   'custom parameter 9','custom parameter 10','custom parameter 11','custom parameter 12']
    custom_inputs = {}
    for c in custom_keys:
      if st.session_state[c] != '' and st.session_state[c] != 0:
        custom_inputs[c] = st.session_state[c]  

    if 'compound_df' not in st.session_state:
      st.session_state['compound_df'] = pd.DataFrame()
    
    row_strings = [st.session_state['key1'],st.session_state['key2'],st.session_state['key3'],st.session_state['key4']]
    row_name = generate_row_name(row_strings)
    st.write(row_name)
    arrays = st.session_state['multi_data_array']
    attributes = st.session_state['single_data']
    decomp_x = st.session_state['multi_data_decompose_x_val']
    decomp_y = st.session_state['multi_data_decompose_y_val']
    if len(decomp_x) != len(decomp_y):
      st.error('Decompositoins must have the same amount of X and Y variables')
    else:
      new_df_row = generate_new_row(row_name,h5_name,selected_sets,attributes,arrays,decomp_x,decomp_y,custom_inputs)

       
      st.subheader('Dataframe snippet (1 row)')
      st.dataframe(new_df_row)

      df_col1, df_col2, df_col3, df_col4 = st.columns((3,3,3,3))
      add_row = df_col1.button('Add snippet to compound dataframe',key = 'add_row')
      delete_last_row = df_col2.button('Delete last row',key = 'delete_last_row')
      clear_df = df_col3.button('Clear dataframe',key = 'clear_df')
      visplore = df_col4.button('Export to Visplore',key = 'visplore')

      if add_row:
        st.session_state['compound_df'] = pd.concat([st.session_state['compound_df'],new_df_row], ignore_index = True)

      if delete_last_row:
        st.session_state['compound_df'] = st.session_state['compound_df'].drop(st.session_state['compound_df'].index[-1])
      
      if clear_df:
        st.session_state['compound_df'] = pd.DataFrame()

        
      st.subheader('Compound dataframe')
      st.dataframe(st.session_state['compound_df'])
      
      #######################################################################################################################
      #######################################################################################################################
      ############# To Do: import Visplore module + implement connection to send the dataframe ##############################
      if visplore:
        st.warning('Connect to Visplore')
        
        df_for_export = st.session_state['compound_df']
      #######################################################################################################################
      #######################################################################################################################
      
