import streamlit as st
import pandas as pd
import numpy as np



def form1():
    global batch
    batch = st.selectbox(
        'select batch?',
        ('2020-2022', '2021-2023', 'Mobile phone'))

    #st.write('You selected:', batch)
    global branch
    global courses
    global sem
    global attdate
    global period
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
    global adf,new
    new=pd.DataFrame(columns=['batch','branch','courses','sem','attdate','period','regdno','attendance'])
    adf={'batch':[],'branch':[],'courses':[],'sem':[],'attdate':[],'period':[],'regdno':[],'attendance':[]}
    data = st.cache(pd.read_csv)('MCA I yr.csv', nrows=100)
    global selected_list
    selected_list=[]
    data_list=data.values.tolist()
    rcount=data.shape[0]
    for row in data_list:
        x=st.checkbox(row[1],value=True)
        selected_list.append(x)

    for c in range(0,rcount):
        adf['batch'].append(batch)
        adf['branch'].append(branch)
        adf['courses'].append(courses)
        adf['sem'].append(sem)
        adf['attdate'].append(attdate)
        adf['period'].append(period)
        adf['regdno'].append(data_list[c][1])
        adf['attendance'].append(selected_list[c])
    new = pd.DataFrame.from_dict(adf)
    new.index = np.arange(1, len(new)+1)
    st.dataframe(new)





@st.cache
def convert_df(df):
    new.index = np.arange(1, len(new)+1)
    return df.to_csv().encode('utf-8')



form1()

display_datagrid()
csv = convert_df(new)
st.download_button(
   "Press to Download",
   csv,
   "file.csv",
   "text/csv",
   key='download-csv'
)