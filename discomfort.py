#Aqara 온습도 센서 불쾌지수 구하기

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import mysql.connector
import seaborn as sns
import streamlit as st
# Load dataset

names = ['Temperature', 'Humidity', 'AirPressure', 'Class']

#connection = mysql.connector.connect(host='112.157.171.74',user='iotuser',password="iot12345", database='iot')
connection = mysql.connector.connect(host='142.93.75.207',user='iotuser',password="iot12345", database='iot')

mycursor = connection.cursor()

sample_size = 1000

mycursor.execute("select temperature, humidity,pressure,discomfort from discomfortTable order by id desc limit {}".format(sample_size))
datasetAqara=pd.DataFrame(list(mycursor))
connection.commit()
datasetAqara.columns = names
datasetAqara = datasetAqara.rename(columns=lambda x: x.strip().lower())

datasetKMA = pd.read_csv("weather7.csv",names=names)
datasetKMA = datasetKMA.rename(columns=lambda x: x.strip().lower())


#g = sns.PairGrid(dataset, hue="class")
#g.map_diag(sns.histplot)
#g.map_offdiag(sns.scatterplot)
#g.add_legend()
#st.pyplot(g)

x = datasetAqara.drop(['class'],axis=1)
y = datasetAqara['class']

# model fit

log_model = LogisticRegression(C=1)
log_model.fit(x,y)

xKMA = datasetKMA.drop(['class'],axis=1)
yKMA = datasetKMA['class']

# model fit

log_modelKMA = LogisticRegression(C=1)
log_modelKMA.fit(xKMA,yKMA)

import pickle
pickle.dump(log_model, open("aqara.sav","wb"))
pickle.dump(log_modelKMA,open("KMA.sav","wb"))




