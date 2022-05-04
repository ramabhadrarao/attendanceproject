import streamlit as st
import pandas as pd
import numpy as np
import mysql.connector
global mydb
global data





def form1():
    st.header("Student Daily Attendance")
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
    global adf,new
    new=pd.DataFrame(columns=['batch','branch','courses','sem','attdate','period','regdno','attendance'])
    adf={'batch':[],'branch':[],'courses':[],'sem':[],'attdate':[],'period':[],'regdno':[],'attendance':[]}
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
    totaldata=new.values.tolist()
    #st.write(totaldata)
    new.index = np.arange(1, len(new)+1)
    new.query("attendance == False",inplace=True)
    absentees=new["regdno"].to_list()
    st.dataframe(new)
    st.warning("Dear Parent today the following student(s) are absent for period:("+str(period)+")"+str(absentees))
    savedata=st.button("save Data")
    showconsolidated=st.button("Show Today consolidated Attendance Regd wise")
    if savedata:
        mycursor = mydb.cursor()
        sql = "INSERT INTO attendance (batch, branch, courses, sem, attdate, period, regdno, attendance) VALUES (%s, %s,%s, %s,%s, %s,%s, %s)"
        checksql="select count(*) from attendance where batch='"+str(batch)+"'and  branch='"+str(branch)+"' and courses='"+str(courses)+"' and sem='"+str(sem)+"' and attdate='"+str(attdate)+"' and period="+str(period)
        #st.write(checksql)
        mycursor.execute(checksql)
        (count,)=mycursor.fetchone()
        #st.write(count)
        if int(count) > 0 :
            st.success("This Attendance is already Saved")
        else:
            for val in totaldata:
                val = (val[0],val[1],val[2],val[3],val[4],val[5],val[6],val[7])
                mycursor.execute(sql, val)
            mydb.commit()
            st.success("Data Saved Succesfully")
    if showconsolidated:
        mycursor2 = mydb.cursor()
        checksql1="select regdno,sum(attendance) from attendance where batch='"+str(batch)+"'and  branch='"+str(branch)+"' and courses='"+str(courses)+"' and sem='"+str(sem)+"' and attdate='"+str(attdate)+"'  group by regdno"
        mycursor2.execute(checksql1)
        myresult=mycursor2.fetchall()
        count=len(myresult)
        if count > 0:
            cons=pd.DataFrame(myresult)
            cons.columns=['Regdno','Total Periods']
            cons["Total Periods"]=cons["Total Periods"].astype(int)
            cons.index = np.arange(1, len(cons)+1)
            st.dataframe(cons)
        else:
            st.warning("Today Attendance Not Taken by Any Faculty")








@st.cache
def convert_df(df):
    new.index = np.arange(1, len(new)+1)
    return df.to_csv().encode('utf-8')



form1()
if branch == "MCA" and sem == "I-I":
        data = st.cache(pd.read_csv)('MCA I yr.csv', nrows=100)
        display_datagrid()
if branch == "MCA" and sem == "II-II":
        data = st.cache(pd.read_csv)('MCA II yr.csv', nrows=100)
        display_datagrid()







        #csv = convert_df(cons)
        #st.download_button("Press to Download", csv, "file.csv", "text/csv",  key='download-csv' )