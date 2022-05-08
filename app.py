import streamlit as st
import pandas as pd
import numpy as np
import mysql.connector
global mydb
global data
global staffsubject

def check_password():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        
        """Checks whether a password entered by the user is correct."""
        if (
            st.session_state["username"] in st.secrets["passwords"]
            and st.session_state["password"]
            == st.secrets["passwords"][st.session_state["username"]]
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 User not known or password incorrect")
        return False
    else:
        # Password correct.
        return True




#########################################################











st.set_page_config(page_title="Swarnandhra", page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)











def form1():
    st.header("Student Daily Attendance")
    global batch
    batch = st.selectbox(
        'select Academics Year?',
        ('2022-2023', '2023-2024', '2024-2025'))

    #st.write('You selected:', batch)
    global branch
    global courses
    global sem
    global attdate
    global period
    global periodtype
    global subject_selected
    global faculty_selected
    global fetch
    branch = st.selectbox(
        'select branch?',
        ('B.Tech', 'M.Tech', 'MCA', 'MBA'))
    if 'branch' not in st.session_state:
        st.session_state.barnch = True
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
    if 'courses' not in st.session_state:
        st.session_state.courses = True
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
    if 'sem' not in st.session_state:
        st.session_state.sem = True
    attdate=st.date_input('Select Date:')
    if 'attdate' not in st.session_state:
        st.session_state.attdate = True
    period=st.number_input('Select Period',min_value=1,max_value=8)
    if 'period' not in st.session_state:
        st.session_state.period = True
    periodtype=st.selectbox("Select Period Type",('Theory','Lab'))
    if 'periodtype' not in st.session_state:
        st.session_state.periodtype = True
    if period > 6 and periodtype == "Lab":
        st.warning("Lab Minimum Periods are 3 so, Lab must start on or before 6th period.Attendance can save period by period Only")
    sas=pd.DataFrame(staffsubject)
    saf_selected=sas.loc[(sas['Course'] == courses) & (sas['Semester'] == sem)]
    faculty=saf_selected['FacultyName'].unique()
    flist=[]
    for fl in faculty:
        flist.append(fl)
    faculty_selected=st.selectbox("Select Faculty",flist)
    if 'faculty_selected' not in st.session_state:
        st.session_state.faculty_selected = True
    #subjects=pd.DataFrame(staffsubject)
    sas_selected=sas.loc[(sas['FacultyName'] == faculty_selected) & (sas['Course'] == courses) & (sas['Semester'] == sem)]
    subjects=sas_selected['Subject'].unique()
    slist=[]
    for sl in subjects:
        slist.append(sl)
    subject_selected=st.selectbox("Select Subject",slist)
    if 'subject_selected' not in st.session_state:
        st.session_state.subject_selected = True
    
    



#https://towardsdatascience.com/make-dataframes-interactive-in-streamlit-c3d0c4f84ccb
    



def display_datagrid():
    global adf,new
    new=pd.DataFrame(columns=['batch','branch','courses','sem','attdate','period','regdno','attendance','subject','faculty','periodtype'])
    adf={'batch':[],'branch':[],'courses':[],'sem':[],'attdate':[],'period':[],'regdno':[],'attendance':[],'subject':[],'faculty':[],'periodtype':[]}
    global selected_list
    selected_list=[]
    data_list=data.values.tolist()
    rcount=data.shape[0]
    #st.dataframe(data_list)
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
        adf['subject'].append(subject_selected)
        adf['faculty'].append(faculty_selected)
        adf['periodtype'].append(periodtype)
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
        sql = "INSERT INTO bietattendance (batch, branch, courses, sem, attdate, period, regdno, attendance,subject,faculty,periodtype) VALUES (%s, %s,%s, %s,%s, %s,%s, %s, %s,%s ,%s)"
        checksql="select count(*) from bietattendance where batch='"+str(batch)+"'and  branch='"+str(branch)+"' and courses='"+str(courses)+"' and sem='"+str(sem)+"' and attdate='"+str(attdate)+"' and period="+str(period)
        #st.write(checksql)
        mycursor.execute(checksql)
        (count,)=mycursor.fetchone()
        #st.write(count)
        if int(count) > 0 :
            st.success("This Attendance is already Saved")
        elif periodtype == "Theory":
                for val in totaldata:
                    val = (val[0],val[1],val[2],val[3],val[4],val[5],val[6],val[7],val[8],val[9],val[10])
                    mycursor.execute(sql, val)
                mydb.commit()
                st.success("Theory Period Attendance Data Saved Succesfully")
        elif periodtype == "Lab" and period > 6:
                for val in totaldata:
                    val = (val[0],val[1],val[2],val[3],val[4],val[5],val[6],val[7],val[8],val[9],val[10])
                    mycursor.execute(sql, val)
                mydb.commit()
                st.success("Theory Period Attendance Data Saved Succesfully")
        elif periodtype == "Lab" and period <=6:
                for val in totaldata:
                    val = (val[0],val[1],val[2],val[3],val[4],val[5],val[6],val[7],val[8],val[9],val[10])
                    mycursor.execute(sql, val)
                    val = (val[0],val[1],val[2],val[3],val[4],val[5]+1,val[6],val[7],val[8],val[9],val[10])
                    mycursor.execute(sql, val)
                    val = (val[0],val[1],val[2],val[3],val[4],val[5]+1,val[6],val[7],val[8],val[9],val[10])
                    mycursor.execute(sql, val)
                mydb.commit()
                st.success("Lab 3 Periods Attendance Data Saved Succesfully")
    if showconsolidated:
        mycursor2 = mydb.cursor()
        checksql1="select regdno,sum(attendance) from bietattendance where batch='"+str(batch)+"'and  branch='"+str(branch)+"' and courses='"+str(courses)+"' and sem='"+str(sem)+"' and attdate='"+str(attdate)+"'  group by regdno"
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


if check_password():
    mydb = mysql.connector.connect(**st.secrets["mysql"])
    staffsubject=st.cache(pd.read_csv)('facultysubjectassignmentcsv.csv', nrows=500)
    form1()
    if branch == "B.Tech"  and courses == "CSE" and sem == "IV-II":
            data = st.cache(pd.read_csv)('cseiv.csv', nrows=100)
            display_datagrid()
                
    if branch == "B.Tech"  and courses == "CSE" and sem == "II-II":
            data = st.cache(pd.read_csv)('cseii.csv', nrows=100)
            display_datagrid()
    if branch == "B.Tech"  and courses == "CSE" and sem == "III-II" and subject_selected:
            data = st.cache(pd.read_csv)('cseiii.csv', nrows=100)
            display_datagrid()
    if branch == "B.Tech"  and courses == "ECE" and sem == "IV-II":
            data = st.cache(pd.read_csv)('eceiv.csv', nrows=100)
            display_datagrid()
    if branch == "B.Tech"  and courses == "ECE" and sem == "II-II":
            data = st.cache(pd.read_csv)('eceii.csv', nrows=100)
            display_datagrid()
    if branch == "B.Tech"  and courses == "ECE" and sem == "III-II":
            data = st.cache(pd.read_csv)('eceiii.csv', nrows=100)
            display_datagrid()
    if branch == "B.Tech"  and courses == "Civil" and sem == "IV-II":
            data = st.cache(pd.read_csv)('civiliv.csv', nrows=100)
            display_datagrid()
    if branch == "B.Tech"  and courses == "Civil" and sem == "III-II":
            data = st.cache(pd.read_csv)('Civiliii.csv', nrows=100)
            display_datagrid()








        #csv = convert_df(cons)
        #st.download_button("Press to Download", csv, "file.csv", "text/csv",  key='download-csv' )