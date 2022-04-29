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
    global data
    data = st.cache(pd.read_csv)('MCA I yr.csv', nrows=100)
    global selected_list
    selected_list=[]
    data_list=data.values.tolist()
    for row in data_list:
        x=st.checkbox(row[1],value=True)
        selected_list.append(x)
        
    st.write(selected_list)





@st.cache
def convert_df(df):
   return df.to_csv().encode('utf-8')



form1()

display_datagrid()
csv = convert_df(data)
st.download_button(
   "Press to Download",
   csv,
   "file.csv",
   "text/csv",
   key='download-csv'
)