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

def gen_fig(X,Y,names,title,x_ax,y_ax,log_x,log_y):

    fig = go.Figure()
    fig.update_layout(width=800, height=600)

    for x,y,name in zip(X,Y,names):     
        fig.add_trace(go.Scatter(x=x, y=y, name=name, mode=st.session_state['plot_type']))  

    fig.update_layout(title=title, xaxis_title=x_ax, \
                    yaxis_title=y_ax)

    if log_y:
        fig.update_layout(yaxis_type='log', yaxis=dict(dtick=1))
        fig.update_yaxes(tickformat="1.1e")

    if log_x:
        fig.update_layout(yaxis_type='log', yaxis=dict(dtick=1))
        fig.update_yaxes(tickformat="1.1e")

    return fig

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

    '''---'''
    selected_sets = []
    plot_axes = []    
    
    plotcol1, plotcol2, plotcol3, plotcol4 = st.columns((3,3,3,3))
    for p in paths:
        plotcol1.checkbox(p,value=True,key=p)
        with h5py.File(h5_name, 'r') as f:
 
            if st.session_state[p]:
                selected_sets.append(p)
                try:
                    for col_name in f[p].dtype.names:
                        if col_name not in plot_axes:
                            plot_axes.append(col_name)

                except:
                   st.warning('Something went wrong when extracting axes to plot.')
                   
    plot = plotcol4.button('Generate plot', key = 'plotting')
    exp_graph = plotcol4.button('Export graph data', key = 'graph_exp')
    exp_sets = plotcol4.button('Export full datasets', key = 'full_exp')
    rep_curve = plotcol4.button('Create Rep. Curve', key = 'rep_curve')    

    plotcol2.selectbox('X-Axis:', plot_axes, key ='X-var')
    plotcol2.selectbox('Y-Axis:', plot_axes, key ='Y-var')
    plotcol2.selectbox('2nd Y-Axis:', plot_axes, key ='Y2-var')
    plotcol2.radio('Plot type:',['lines','markers','lines+markers'],key = 'plot_type')
    
    plotcol3.subheader('')
    plotcol3.subheader('')
    plotcol3.checkbox('Log. X-Scaling:',value=False,key='X-scale')
    plotcol3.subheader('')
    plotcol3.subheader('')
    plotcol3.checkbox('Log. Y-Scaling:',value=False,key='Y-scale')
    plotcol3.subheader('')
    plotcol3.checkbox('Use 2nd Y-Axis:',value=False,key='use-Y2')
    plotcol3.checkbox('Log. Y2-Scaling:',value=False,key='Y2-scale')
    
    
    
    if plot:     
        #st.experimental_rerun()       
        X = []
        Y = []
        names = []
        x_ax = st.session_state['X-var']
        y_ax = st.session_state['Y-var']
        log_x = st.session_state['X-scale']
        log_y = st.session_state['Y-scale']
        title = 'Titel - Ideen? Brauch ma den?'
        with h5py.File(h5_name, 'r') as f:
            for set in selected_sets:
                ds = f[set]
                if x_ax in ds.dtype.names and y_ax in ds.dtype.names:
                    X.append(ds[x_ax])
                    Y.append(ds[y_ax])
                    names.append(set)
                else:
                    plotcol3.write(f'{set} did not have the selected columns.')


        try:            
            figure_try = gen_fig(X,Y,names,title,x_ax,y_ax,log_x,log_y)
            st.plotly_chart(figure_try, use_container_width=True, theme = 'streamlit')
        except:
            keycol3.warning('No data selected.')

    
    if rep_curve:
        plotcol4.success('blending curves')
        with h5py.File(h5_name, 'r') as f:
            collective = {}
            #rep_path = selected_sets[0]+'_rep'
            #grp = f.require_group(combo_path)
            #ds = grp.create_dataset(ds_name, data = data, compression="gzip", compression_opts=9) 
            
            rep = f[selected_sets[0]]
            for col_name in rep.dtype.names:
                collective[col_name] = np.ndarray((len(selected_sets),len(rep)))
                for ind,set in enumerate(selected_sets):
                    collective[col_name][ind,:] = f[set][col_name]
            # for k,v in collective.items():
            #     rep[k] = np.mean(v,axis=0)


            st.write(collective)
            st.write(rep)
                
        
    if exp_graph:
        plotcol3.success('graph exp')

    if exp_sets:
        plotcol3.success('sets exp')

