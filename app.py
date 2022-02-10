import streamlit as st
from predict_page import show_predict_page
from explore_page import show_explore_page
from model_page import show_model_page
#from deep_page import show_deep_page
#from cnn_page import show_cnn_page
from deeplearning_page import show_deeplearning_page
from autoML_page import show_autoML_page
from mysql_page import show_mysql_page
from PIL import Image
import mysql.connector

connection = mysql.connector.connect(host='142.93.75.207',user='iotuser',password="iot12345", database='iot')
mycursor = connection.cursor()
    
sample_size = 2
    
mycursor.execute("select temperature, humidity,pressure,discomfort from discomfortTable order by id desc limit {}".format(sample_size))
lastData=list(mycursor)
print(lastData[0][2])
print(lastData[1][2])
connection.commit()
image = Image.open("aqara.png")
st.sidebar.image(image,width = 200)
st.write("""### Aqara 온습도센서 Live Data""")
col1,col2,col3 = st.columns(3)
col1.metric("온도",str(lastData[0][0])+" ℃",str(lastData[0][0]-lastData[1][0])+" ℃")
col2.metric("습도",str(lastData[0][1]) + " %",str(lastData[0][1]-lastData[1][1])+ " %")
col3.metric("기압",str(lastData[0][2]) + " hPa",str(lastData[0][2]-lastData[1][2])+ " hPa")

page=st.sidebar.selectbox("Explore or Predict using Aqara THP",("Predict","Explore","Model Evaluation","Deep Learning","Database","AutoML"))

if page == "Predict":
    show_predict_page()
elif page == "Explore":
    show_explore_page()
elif page =="Model Evaluation":
    show_model_page()
elif page =="Deep Learning":
    show_deeplearning_page()
elif page == "Database":
    show_mysql_page()
elif page == "AutoML":
    show_autoML_page()  

    


    
