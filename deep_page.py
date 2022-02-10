from os import name
import streamlit as st
import pandas as pd
import matplotlib 
import seaborn as sns
import pickle
import mysql.connector
import pandas as pd
import sklearn
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
import seaborn as sns
import tensorflow as tf
import numpy as np
from sklearn.preprocessing import LabelEncoder

# Load dataset
@st.cache
def load_data():
    names = ['Temperature', 'Humidity', 'AirPressure', 'Class']
    connection = mysql.connector.connect(host='142.93.75.207',user='iotuser',password="iot12345", database='iot')
    #connection = mysql.connector.connect(host='112.157.171.74',port="23306",user='iotuser',password="iot12345", database='iot')

    mycursor = connection.cursor()
    
    sample_size = 1000
    
    mycursor.execute("select temperature, humidity,pressure,discomfort from discomfortTable order by id desc limit {}".format(sample_size))
    datasetAqara=pd.DataFrame(list(mycursor))
    connection.commit()
    
    datasetAqara.columns = names
    datasetAqara = datasetAqara.rename(columns=lambda x: x.strip().lower())

    datasetKMA = pd.read_csv("weather7.csv",names=names)
    datasetKMA = datasetKMA.rename(columns=lambda x: x.strip().lower())

    return datasetAqara,datasetKMA


datasetAqara, datasetKMA = load_data()
print (type(datasetAqara),type(datasetKMA))

subdataAqara = datasetAqara[["temperature","humidity","airpressure"]]
subdataKMA = datasetKMA[["temperature","humidity","airpressure"]]



def show_deep_page():
    st.title("Deep Learning")
    st.write("""### Based on Aqara THP Data or KMA Data""")
    
    
    chooseDB = st.selectbox("Aqara DB or KMA DB",("KMA DB","Aqara DB"))
    #choosePlot=st.selectbox("Correlation chart, bar chart or data frame",("Correlation","Bar Chart", "Data Frame"))

    

# Data Summary


    if chooseDB == "KMA DB":
            dataset = datasetKMA
            subdata = subdataKMA
    elif chooseDB == "Aqara DB":
            dataset = datasetAqara
            subdata = subdataAqara
    
    print("test1",datasetKMA)
    print("test2",datasetAqara)



# Seperation of Dataset
    #array = dataset.values
    #X = array[:,0:3]
    #yy = array[:,3]

    X = dataset.iloc[:,0:3]
    y = dataset.iloc[:,3]
    validation_size = 0.10
    seed = 7
    print(y)
    encorder = LabelEncoder()
    y1 = encorder.fit_transform(y)
    print(y1)
    Y= pd.get_dummies(y1).values
    X_train,X_validation,y_train,y_validation = model_selection.train_test_split(
        X,Y,test_size= validation_size,stratify=y,random_state = seed)
    

    
    model = tf.keras.models.Sequential()
    no_of_layers = st.slider("No. of Layers", min_value=2, max_value=10,value=3,step=1)
    no_of_nodes = st.slider("No. of Nodes from Each Layer",min_value=2, max_value=10,value=3,step=1 )
    batch_size = st.slider("Batch Size", min_value=10, max_value=100,value=50,step=10)
    epochs = st.slider("No. of Epochs", min_value=100, max_value=1000,value=200,step=100)

    for iteration in range(no_of_layers-1):
        model.add(
            tf.keras.layers.Dense(units=no_of_nodes,
                                input_dim=X_train.shape[1],
                                activation='relu')
        )

    model.add(
        tf.keras.layers.Dense(units=3,
                              activation='softmax')
    )
    #st.text_area("Model Summary",model.summary(),height=100)
    
    

    optimizer = tf.keras.optimizers.SGD(learning_rate=0.01,
                                        momentum=0.9,
                                        nesterov=True)
    model.compile(optimizer = optimizer,
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    
    model.fit(X_train,y_train,batch_size=batch_size,epochs=epochs)
    loss,accuracy = model.evaluate(X_validation,y_validation, verbose=0)
    print('Test loss:', loss)
    print("Test accuracy:", accuracy)
    #st.text_area("Epochs Progress",epochs_progress,height=300)
    st.text_area("Loss",loss,height=100)
    st.text_area("Accuracy",accuracy,height=100)
    y_pred = model.predict(X_validation)


    temperature = st.slider("Temperature", min_value=-20, max_value=50,value=10,step=1)
    humidity = st.slider("Humidity", min_value=1, max_value=99,value=30, step=1)
    air_pressure = st.slider("Air Pressure", min_value=900, max_value=1200, value=1000,step=10)

    #ok = st.button("Predict Discomfort Index")
    
    ok = st.button("Predict Discomfort Index")
    if ok:
        #X = np.arrary([[temperature,humidity,air_pressure]])
        feelbad = np.array([[1,0,0]])
        feelgood = np.array([[0,1,0]])
        feelsoso = np.array([[0,1,0]])
        prediction = model.predict([[temperature,humidity,air_pressure]])
        print("first:",prediction[0,0])
        print("second",prediction[0,1])
        print("third",prediction[0,2])
        if (prediction[0,0] > 0.35):
            decision = "Uncomfortable"
        elif (prediction[0,1] > 0.35):
            decision = "Comfortable"
        elif (prediction[0,2] > 0.35):
            decision = "So-So"
        else:
            decision = "Unpredictable"
            return "error"
        #st.subheader("The estimated discomfort index is ${discomfort_index[0]}")
    
        st.write("Discomfort Index Below")
    
        st.subheader(decision)
    print(no_of_layers)



