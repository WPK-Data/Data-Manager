import streamlit as st
import numpy as np
import pandas as pd
import os
import plotly.graph_objects as go
import h5py


#when add dataset button is pressed:
def add_measurement(data,h5_file,combo_path,ds_name,comment,attributes):

    with h5py.File(h5_file.name, 'a') as f:

        node = combo_path + '/' + ds_name
        #Eintrag löschen, falls es ihn vorher schon gegeben hat ==> überschreiben

        if node in f.keys():
            del f[node]
            st.write(f'The specimen {node} already existed and was overwritten with the new data.')
        
        grp = f.require_group(combo_path)
        
        ds = grp.create_dataset(ds_name, data = data, compression="gzip", compression_opts=9) 
        print(ds) 
        
        ds.attrs['Comment'] = comment
        
        for att in attributes:
            ds.attrs[att] = st.session_state[att]
        
            
    st.success(f'Dataset {node} was added.')


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

#''' ------------------------------- '''


#''' Dictionaries with operational settings'''
machines = {
    'Zwick':{'methods':['tensile','pressure','creep'],
             'headers':0,
             'dec':',',  
             'sep':','},
    'MTS':{'methods':['tensile','pressure','fatigue'],
             'headers':0,
             'dec':',',  
             'sep':','},
    'Instron':{'methods':['tensile','pressure','creep'],
             'headers':0,
             'dec':',',  
             'sep':','},
    'Mettler':{'methods':['DMA','DSC'],
             'headers':0,
             'dec':',',  
             'sep':','},
    'Mistras':{'methods':['AE-tensile','AE-fatigue'],
             'headers':0,
             'dec':'.',  
             'sep':','},
    'Mercury':{'methods':['tensile','pressure','creep'],
             'headers':0,
             'dec':',',  
             'sep':','},
    'IR-machine':{'methods':['FTIR (refl.)'],
             'headers':24,
             'dec':'.',              
             'sep':'\t'},
    'CRB':{'methods':['CRB-series'],
             'headers':62,
             'dec':'.',              
             'sep':';'},
    }
A = {
    'name':'A [-]',
    'type':'numeric',
    'min_value':0.0,
    'max_value':10000.0,
    'value':0.0,
    'step':10**-5
} 

B = {
    'name':'B [-]',
    'type':'numeric',
    'min_value':0.0,
    'max_value':10000.0,
    'value':0.0,
    'step':10**-5
}

C = {
    'name':'C [-]',
    'type':'numeric',
    'min_value':0.0,
    'max_value':10000.0,
    'value':0.0,
    'step':10**-5
} 

H = {
    'name':'H [mm]',
    'type':'numeric',
    'min_value':0.0,
    'max_value':10000.0,
    'value':0.0,
    'step':10**-5
} 

L = {
    'name':'L [mm]',
    'type':'numeric',
    'min_value':0.0,
    'max_value':10000.0,
    'value':0.0,
    'step':10**-5
} 

X = {
    'name':'X [mm]',
    'type':'numeric',
    'min_value':0.0,
    'max_value':10000.0,
    'value':0.0,
    'step':10**-5
} 

Y = {
    'name':'Y [mm]',
    'type':'numeric',
    'min_value':0.0,
    'max_value':10000.0,
    'value':0.0,
    'step':10**-5
} 

Z = {
    'name':'Z [-]',
    'type':'numeric',
    'min_value':0.0,
    'max_value':10000.0,
    'value':0.0,
    'step':10**-5
} 

m = {
    'name':'m [-]',
    'type':'numeric',
    'min_value':0.0,
    'max_value':10000.0,
    'value':0.0,
    'step':10**-5
} 

n = {
    'name':'n [-]',
    'type':'numeric',
    'min_value':0.0,
    'max_value':10000.0,
    'value':0.0,
    'step':10**-5
} 

z = {
    'name':'z [-]',
    'type':'numeric',
    'min_value':0.0,
    'max_value':10000.0,
    'value':0.0,
    'step':10**-5
} 

R_ratio = {
    'name':'R-ratio [-]',
    'type':'numeric',
    'min_value':0.0,
    'max_value':10.0,
    'value':0.0,
    'step':0.1
} 

page = {
    'name':'Sheet Nr.',
    'type':'numeric',
    'min_value':1,
    'max_value':100,
    'value':1,
    'step':1
} 

attributes = {
    'tensile':[B,H,L],
    'pressure':[X,Y,Z],
    'creep':[A,B,C],
    'AE-tensile':[B,H,L],
    'AE-fatigue':[B,H,L],
    'DMA':[B,H,L],
    'DSC':[B,H,L],
    'FTIR (refl.)':[],
    'CRB-series':[page,R_ratio,A,m,B,n,C,z]
    }

precise_float = np.float64  #decimal number with a large number of digits
medium_float = np.float32   #decimal number with a medium number of digits
coarse_float = np.float16   #decimal number with a lower number of digits
precise_int = np.int64      #integer number with a large number of digits
medium_int = np.int32       #integer number with a medium number of digits
coarse_int = np.int16       #integer number with a lower number of digits

def generate_data():
    for f in st.session_state.uploads:
        #st.write(f)
                
        if f.name == st.session_state['spec_list'] and st.session_state['method'] == 'AE-tensile':
            data = generate_AE_tensile(f, machines[st.session_state['machine']]['headers'],machines[st.session_state['machine']]['sep'],machines[st.session_state['machine']]['dec'])
            break

        elif f.name == st.session_state['spec_list'] and st.session_state['method'] == 'FTIR (refl.)':
            data = generate_FTIR(f, machines[st.session_state['machine']]['headers'],machines[st.session_state['machine']]['sep'],machines[st.session_state['machine']]['dec'])
            break

        elif f.name == st.session_state['spec_list'] and st.session_state['method'] == 'CRB-series':
            data = generate_CRB_series(f, machines[st.session_state['machine']]['headers'],machines[st.session_state['machine']]['sep'],machines[st.session_state['machine']]['dec'])
            break
            
    return data

def generate_CRB_series(file_raw, header, sep, dec):
  
    # features: not applicable for FTIR:no column names given!
    D_type = np.dtype(
        ### structure of data type: #################################################
        #   using compound data type for better structure in hdf5 file
        #   type = [(variable name (must match features!), precision)]
        #############################################################################        
        [('wave number [1/cm]',coarse_int),                        
        ('reflection [%]',precise_float),
        ('normalized reflection [-]',precise_float),
        ])
    
    Nas = ['']     #needed or not? ['MPa','%','N','mm','s']
    df = pd.read_csv(file_raw, header = header, sep = sep, na_values = Nas, decimal = dec, index_col = None) #, encoding = 'utf-8'                    
    data = np.zeros(len(df), dtype = D_type) #initialize as zeros; if one col is not found, it stays as 0s

    data['wave number [1/cm]'] = df.index.values #1000 separator appears as ','....no idea why )-:; but is numerically correct!
    data['reflection [%]'] = df.iloc[:,0].to_numpy()
    data['normalized reflection [-]'] = (data['reflection [%]']-np.mean(data['reflection [%]']))/np.std(data['reflection [%]'])

    #alternatively: force to 0-1 space
    #data['normalized reflection [-]'] = data['reflection [%]']-min(data['reflection [%]']) # shift, so that minimum is at 0
    #data['normalized reflection [-]'] = data['normalized reflection [-]']/max(data['normalized reflection [-]']) #normalize by max-value

    return data

def generate_FTIR(file_raw, header, sep, dec):
  
    # features: not applicable for FTIR:no column names given!
    D_type = np.dtype(
        ### structure of data type: #################################################
        #   using compound data type for better structure in hdf5 file
        #   type = [(variable name (must match features!), precision)]
        #############################################################################        
        [('wave number [1/cm]',coarse_int),                        
        ('reflection [%]',precise_float),
        ('normalized reflection [-]',precise_float),
        ])
    
    Nas = ['']     #needed or not? ['MPa','%','N','mm','s']
    df = pd.read_csv(file_raw, header = header, sep = sep, na_values = Nas, decimal = dec, index_col = None) #, encoding = 'utf-8'                    
    data = np.zeros(len(df), dtype = D_type) #initialize as zeros; if one col is not found, it stays as 0s

    data['wave number [1/cm]'] = df.index.values #1000 separator appears as ','....no idea why )-:; but is numerically correct!
    data['reflection [%]'] = df.iloc[:,0].to_numpy()
    data['normalized reflection [-]'] = (data['reflection [%]']-np.mean(data['reflection [%]']))/np.std(data['reflection [%]'])

    #alternatively: force to 0-1 space
    #data['normalized reflection [-]'] = data['reflection [%]']-min(data['reflection [%]']) # shift, so that minimum is at 0
    #data['normalized reflection [-]'] = data['normalized reflection [-]']/max(data['normalized reflection [-]']) #normalize by max-value

    return data

   
def generate_AE_tensile(file_raw, header,sep,dec):
    
    features = {
        ### structure of feature collection: #################################################
        #   features = {'key':'value'}
        #   key == name, which will be used from here on
        #   value == [Names to look for in the raw data file]
        ######################################################################################
        'signal amplitude [mV]':['amplitude [mV]'],
        'signal amplitude [dBae]':['amplitude [dBae]'],
        'absolute energy [J]':['absolute energy'],
        'counts to peak':['counts to peak'],
        'counts':['counts'],
        'duration [\u03BCs]':['duration'],
        'rise time [\u03BCs]':['rise time'],
        'average frequency [Hz]':['average frequency'],
        'reverberation frequency [Hz]':['reverberation frequency'],
        'initiation frequency [Hz]':['initiation frequency'],
        'partial power 1 [%]':['partial power 1'],
        'partial power 2 [%]':['partial power 2'],
        'partial power 3 [%]':['partial power 3'],
        'partial power 4 [%]':['partial power 4'],
        'partial power 5 [%]':['partial power 5'],
        'partial power 6 [%]':['partial power 6'],
        'peak frequency [Hz]':['peak frequency'],
        'frequency centroid [Hz]':['frequency centroid'],
        'weighted peak frequency [Hz]':['weighted peak frequency'],        
        'root-mean-square [V]':['root-mean-square'],
        'average-signal-level [dBae]':['average-signal-level'],
        'channel number':['channel'],
        'signal number':['signal number'],
        'hits':['hits'],
        'force [N]':['Force'],
        'displacement [mm]':['displacement'],
        'time [s]':['time'],
        'x [mm]':['x']
        }

    D_type = np.dtype(
        ### structure of data type: #################################################
        #   using compound data type for better structure in hdf5 file
        #   type = [(variable name (must match features!), precision)]
        #############################################################################        
        [('time [s]',coarse_float),
        ('force [N]',coarse_float),
        ('displacement [mm]',coarse_float),
        ('stress [MPa]',coarse_float),
        ('strain [%]',coarse_float),                        
        ('signal amplitude [mV]',coarse_float),
        ('signal amplitude [dBae]',coarse_float),                        
        ('absolute energy [J]',precise_float),  
        ('cumulative energy [J]',precise_float), 
        ('root-mean-square [V]',coarse_float),
        ('average-signal-level [dBae]',coarse_float),                       
        ('average frequency [Hz]',precise_float),
        ('peak frequency [Hz]',precise_float),                        
        ('frequency centroid [Hz]',precise_float),
        ('weighted peak frequency [Hz]',precise_float),                         
        ('partial power 1 [%]',coarse_float),
        ('partial power 2 [%]',coarse_float),
        ('partial power 3 [%]',coarse_float),
        ('partial power 4 [%]',coarse_float),
        ('partial power 5 [%]',coarse_float),
        ('partial power 6 [%]',coarse_float),
        ('hits',medium_int),   
        ('channel number',medium_int),
        ('signal number',medium_int),
        ('duration [\u03BCs]',precise_float),                                             
        ('counts',medium_int),
        ('counts to peak',medium_int),   
        ('rise time [\u03BCs]',precise_float),                        
        ('reverberation frequency [Hz]',precise_float),
        ('initiation frequency [Hz]',precise_float),
        ('x [mm]',coarse_float)
        ])
    
    # standardized block to look for columns and transform them to the specified data type
    Nas = ['']     #needed or not? ['MPa','%','N','mm','s']
    df = pd.read_csv(file_raw, header = header, sep = sep, na_values = Nas,decimal = dec) #, encoding = 'utf-8'                    
    data = np.zeros(len(df), dtype = D_type) #initialize as zeros; if one col is not found, it stays as 0s
    for col in df.columns:
        for ft_final,ft_raw in features.items(): #look for snippets of col-names in raw file and order to final features
            for ft in ft_raw:
                if ft in col:
                    data[ft_final] = df[col].to_numpy()
                    break
                
    
    # columns specific for this type of measurement; maybe outsource to other method for re-evaluation?
    data['strain [%]'] = (data['displacement [mm]']-data['displacement [mm]'][0])/st.session_state['L']
    data['stress [MPa]'] = data['force [N]']/st.session_state['B']/st.session_state['H']
    data['cumulative energy [J]'][0] = data['absolute energy [J]'][0]
    for j in range(1,len(data)):
        data['cumulative energy [J]'][j] = data['cumulative energy [J]'][j-1] + data['absolute energy [J]'][j]   
    
    return data

#''' ------------------------------- '''

st.session_state['upl_rdy'] = False

##############  specify file ###############
if 'h5_file' not in st.session_state:
    st.sidebar.error('No database selected!')
    st.error('No database selected!')
else:
    h5_file = st.session_state['h5_file']
    h5_name = st.session_state['h5_file'].name
    st.success(f'Selected database: {h5_name}')
    st.sidebar.success(f'Selected database: {h5_name}')
    #''' ------------------------------- '''
    ############## ---------------------- ###############

    #''' Test setup '''
    with st.expander('Select test setup'):
        col1,col2 = st.columns(2)    
        col1.selectbox('select machine',machines.keys(),key='machine')
        col2.selectbox('select test method',machines[st.session_state['machine']]['methods'],key='method')
    #''' ------------------------------- '''


    with st.expander('Select architecture'):
        st.number_input('Layer depth', min_value = 0, max_value = 3, value = 3, step=1, key='depth')

        with h5py.File(h5_file.name, 'a') as f:            
        
            with st.container():   
                col3,col4,col7,col8 = st.columns([6,6,2,2])
                col3.selectbox('Select layer',f.keys(),key='L0')
                col4.text_input('Set layer',key = 'L0_new',placeholder = 'Create or delete subfolder')
                col7.text('Add')
                col8.text('Delete')
                L0_add = col7.button(':heavy_plus_sign:',key='L0_add_button')
                L0_rem = col8.button(':skull:',key='L0_rem_button')

                
                if L0_add and st.session_state['L0_new'] != '':
                    #st.experimental_rerun()
                    f.require_group(st.session_state['L0_new'])
                    st.experimental_rerun()

                if L0_rem and st.session_state['L0_new'] != '':
                    #st.experimental_rerun()
                    node = st.session_state['L0_new']
                    if node in f.keys() and 'root' not in node and 'Root' not in node:
                        del f[node]
                    st.experimental_rerun()
                '''---'''
            if st.session_state.depth > 0:
                with st.container():  
                    try:
                        sel = f[st.session_state.L0].keys()
                    except:
                        sel = ''
                    
                    col9,col10,col11,col12 = st.columns([6,6,2,2])      
                    col9.selectbox('select first layer',sel,key='L1',label_visibility = 'collapsed')
                    col10.text_input('a',key = 'L1_new',placeholder = 'Create or delete subfolder',label_visibility = 'collapsed')
                    L1_add = col11.button(':heavy_plus_sign:',key='L1_add_button')
                    L1_rem = col12.button(':skull:',key='L1_rem_button')

                    if L1_add and st.session_state['L1_new'] != '':
                        #st.experimental_rerun()
                        f[st.session_state.L0].require_group(st.session_state['L1_new'])
                        st.experimental_rerun()

                    if L1_rem and st.session_state['L1_new'] != '':
                        #st.experimental_rerun()
                        node = st.session_state.L0+'/'+st.session_state.L1
                        if node in f.keys():
                            del f[node]
                        st.experimental_rerun()
                    '''---'''
            if st.session_state.depth > 1:
                with st.container(): 
                    try:
                        sel = f[st.session_state.L0][st.session_state.L1].keys()
                    except:
                        sel = ''
                    col13,col14,col15,col16 = st.columns([6,6,2,2])
                    col13.selectbox('select second layer',sel,key='L2',label_visibility = 'collapsed')
                    col14.text_input('a',key = 'L2_new',placeholder = 'Create or delete subfolder',label_visibility = 'collapsed')
                    L2_add = col15.button(':heavy_plus_sign:',key='L2_add_button')
                    L2_rem = col16.button(':skull:',key='L2_rem_button')


                    if L2_add and st.session_state['L2_new'] != '':
                        #st.experimental_rerun()
                        f[st.session_state.L0][st.session_state.L1].require_group(st.session_state['L2_new'])
                        st.experimental_rerun()


                    if L2_rem and st.session_state['L2_new'] != '':
                        #st.experimental_rerun()
                        node = st.session_state.L0+'/'+st.session_state.L1+'/'+st.session_state.L2
                        if node in f.keys():
                            del f[node]
                        st.experimental_rerun()

                    '''---'''
            if st.session_state.depth > 2:      
                with st.container(): 
                    try:
                        sel = f[st.session_state.L0][st.session_state.L1][st.session_state.L2].keys()
                    except:
                        sel = ''
                    col17,col18,col19,col20 = st.columns([6,6,2,2])
                    col17.selectbox('select third layer',sel,key='L3',label_visibility = 'collapsed')
                    col18.text_input('a',key = 'L3_new',placeholder = 'Create or delete subfolder',label_visibility = 'collapsed')
                    L3_add = col19.button(':heavy_plus_sign:',key='L3_add_button')
                    L3_rem = col20.button(':skull:',key='L3_rem_button')    

                
                    if L3_add and st.session_state['L3_new'] != '':
                        #st.experimental_rerun()
                        f[st.session_state.L0][st.session_state.L1][st.session_state.L2].require_group(st.session_state['L3_new'])
                        st.experimental_rerun()
                    

                    if L3_rem and st.session_state['L3_new'] != '':
                        #st.experimental_rerun()
                        node = st.session_state.L0+'/'+st.session_state.L1+'/'+st.session_state.L2+'/'+st.session_state.L3
                        if node in f.keys():
                            del f[node]
                        st.experimental_rerun()

                    '''---'''


    if st.session_state.depth == 3:  
        try:
            combo_path = st.session_state.L0+'/'+st.session_state.L1+'/'+st.session_state.L2+'/'+st.session_state.L3
            st.session_state.upl_rdy = True
            st.success(f'Target path: {combo_path}')
        except:
            st.error('No valid path given!')
            st.session_state.upl_rdy = False

    elif st.session_state.depth == 2:  
        try:
            combo_path = st.session_state.L0+'/'+st.session_state.L1+'/'+st.session_state.L2
            st.session_state.upl_rdy = True
            st.success(f'Target path: {combo_path}')
        except:
            st.error('No valid path given!')
            st.session_state.upl_rdy = False

    elif st.session_state.depth == 1:  
        try:
            combo_path = st.session_state.L0+'/'+st.session_state.L1
            st.session_state.upl_rdy = True
            st.success(f'Target path: {combo_path}')
        except:
            st.error('No valid path given!')
            st.session_state.upl_rdy = False

    elif st.session_state.depth == 0:  
        try:
            combo_path = st.session_state.L0
            st.session_state.upl_rdy = True
            st.success(f'Target path: {combo_path}')
        except:
            st.error('No valid path given!')
            st.session_state.upl_rdy = False

    #''' ------------------------------- '''

if st.session_state.upl_rdy:
    #''' File Uploader'''
    #st.header('File Selection')
    if 'uploads' not in st.session_state:
        st.session_state['uploads'] = []
    st.session_state.uploads = st.file_uploader('Choose raw data file(s)',accept_multiple_files = True)
    #st.write(uploaded_files)
    #'---'
    #''' ------------------------------- '''

    #''' Add datasets'''
    if len(st.session_state.uploads)>0:
        with st.expander('Single datasets'):

            col5,col6 = st.columns([8,2])
            file_list = []
            for f in st.session_state.uploads:
                file_list.append(f.name)
            col5.radio('Specimen selection', key = 'spec_list',options = file_list)
            preview = col6.button('Show preview')
            if preview:
                try:
                    data_prev = generate_data()
                    st.dataframe(data_prev)
                except Exception as e:
                    st.error('Something went wrong!')
                    st.write(e)
                    

    
            col24, col25 = st.columns([7,3])

            col24.text_input('Dataset name',placeholder='Give your dataset a name',key='given_name')
            col24.text_input('Comment',placeholder='Enter a comment; what went right or wrong?',key='comment')

            for att in attributes[st.session_state['method']]:
                if att['type'] == 'numeric':
                    col25.number_input(att['name'],value=att['value'],min_value=att['min_value'],max_value=att['max_value'],step=att['step'],key=att['name'])
                if att['type'] == 'text':
                    col25.number_input(att['name'],key=att['name'],placeholder = 'enter text here')
            
            '---'
            add = st.button('Add dataset')
            if add:
                try:
                    data = generate_data()
                    add_measurement(data,h5_file,combo_path,st.session_state.given_name,st.session_state.comment,attributes[st.session_state['method']])
                    
                except Exception as e:
                    st.error('Something went wrong!')
                    st.write(e)

        with st.expander('Multiple datasets'):
            col21,col22,col23 = st.columns([3,3,3])
            col21.button('TestXpert',key='zwick_button')
            col22.button('Template',key='template_button')
            col23.button('Re-use same parameters',key='all_same_button')
        
            
    else:
        st.warning('No files selected!')

    #''' ------------------------------- '''


