import streamlit as st
import mysql.connector
import pandas as pd
from pandas.plotting import scatter_matrix


def show_mysql_page():
    st.title("Database Query")
    st.write("""### Based on Aqara THP Data """)
    
    names = ['Temperature', 'Humidity', 'AirPressure', 'Class']
    connection = mysql.connector.connect(host='142.93.75.207',user='iotuser',password="iot12345", database='iot')

    mycursor = connection.cursor()
    
    sample_size = 1000
    
    mycursor.execute("select temperature, humidity,pressure,discomfort from discomfortTable order by id desc limit {}".format(sample_size))
    datasetAqara=pd.DataFrame(list(mycursor))
    Show_Columns = "show columns from discomfortTable"
    select_all = "select * from discomfortTable"
    select_latest = "select * from discomfortTable order by id desc limit 10"
    select_average = "select avg(temperature),avg(humidity) from discomfortTable"
    chooseStatement = st.selectbox("Choose Statement",('',Show_Columns,select_all,select_latest,select_average))

    
    result_box = st.empty()
    query_box = st.empty()
    query = query_box.text_input("Query Statement")
    
    query = query_box.text_input("Query Statement",value='',key=1) 
    ok = st.button("Database Query")

    query_statement = chooseStatement
    
    if query or ok:
        mycursor.execute(query)
        datasetAqara=pd.DataFrame(list(mycursor))
        st.text_area("Query Result",pd.DataFrame.to_string(datasetAqara),height=300)
        connection.commit()
    if query_statement:
        mycursor.execute(query_statement)
        datasetAqara=pd.DataFrame(list(mycursor))
        result_box.text_area("Query Result",pd.DataFrame.to_string(datasetAqara),height=300)
        connection.commit()
    
    return datasetAqara

dataset = show_mysql_page()


    
