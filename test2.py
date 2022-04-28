import streamlit as st
import pandas as pd
import numpy as np
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode



def form1():
    batch = st.selectbox(
        'select batch?',
        ('2020-2022', '2021-2023', 'Mobile phone'))

    #st.write('You selected:', batch)
    branch = st.selectbox(
        'select branch?',
        ('B.Tech', 'M.Tech', 'MCA', 'MBA'))
    if branch == 'B.Tech':
        courses = st.selectbox(
            'select courses?',
            ('CSE', 'AIML', 'ECE', 'EEE','Mechanical','Civil'))
    if branch == 'M.Tech':
        courses = st.selectbox(
            'select courses?',
            ('CSE', 'SE'))
    if branch == 'MCA':
        courses = st.text_input(
            'select courses?',
            value='MCA',
            disabled=True
            )
    if branch == 'MBA':
        courses = st.text_input(
            'select courses?',
            value='MBA',
            disabled=True
            )
    if branch == 'B.Tech':
        sem = st.selectbox(
            'select Semester?',
            ('I-I', 'I-II', 'II-I', 'II-II','III-I','III-II', 'IV-I','IV-II'))
    if branch == 'M.Tech':
        sem = st.selectbox(
            'select Semester?',
            ('I-I', 'I-II', 'Project Year'))
    if branch == 'MCA':
        sem = st.selectbox(
            'select Semester?',
            ('I-I', 'I-II', 'II-I', 'II-II'))
    if branch == 'MBA':
        sem = st.selectbox(
            'select Semester?',
            ('I-I', 'I-II', 'II-I', 'II-II'))
    attdate=st.date_input('Select Date:')
    period=st.number_input('Select Period',min_value=1,max_value=8)


#https://towardsdatascience.com/make-dataframes-interactive-in-streamlit-c3d0c4f84ccb
    



def display_datagrid():
    data = st.cache(pd.read_csv)('MCA I yr.csv', nrows=100)

    # Select some rows using st.multiselect. This will break down when you have >1000 rows.
    st.write('### Full Dataset', data)
    selected_indices = st.multiselect('Select rows:', data.index)
    global selected_rows
    selected_rows = data.loc[selected_indices]
    st.write('### Selected Rows', selected_rows)        
    





@st.cache
def convert_df(df):
   return df.to_csv().encode('utf-8')



form1()

display_datagrid()
csv = convert_df(selected_rows)
st.download_button(
   "Press to Download",
   csv,
   "file.csv",
   "text/csv",
   key='download-csv'
)