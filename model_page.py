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
subdataAqara = datasetAqara[["temperature","humidity","airpressure"]]
subdataKMA = datasetKMA[["temperature","humidity","airpressure"]]



def show_model_page():
    st.title("Evaluate Models")
    st.write("""### Based on Aqara THP Data or KMA Data""")
    chooseDB = st.selectbox("Aqara DB or KMA DB",("KMA DB","Aqara DB"))
    #choosePlot=st.selectbox("Correlation chart, bar chart or data frame",("Correlation","Bar Chart", "Data Frame"))
    if chooseDB == "KMA DB":
            dataset = datasetKMA
            subdata = subdataKMA
    elif chooseDB == "Aqara DB":
            dataset = datasetAqara
            subdata = subdataAqara

    

# Data Summary


    if chooseDB == "KMA DB":
            dataset = datasetKMA
            subdata = subdataKMA
    elif chooseDB == "Aqara DB":
            dataset = datasetAqara
            subdata = subdataAqara
    st.text_area("Dataset Shape",dataset.shape,height=100)
    st.text_area("Latest Dataset",pd.DataFrame.to_string(dataset.head(10)),height=300)
    st.text_area("Description of Dataset",pd.DataFrame.to_string(dataset.describe()),height=300)
    

#Data Visualization
    st.write("""### Pair Grid Chart for Correlation""")
    g = sns.PairGrid(dataset, hue="class")
    g.map_diag(sns.histplot)
    g.map_offdiag(sns.scatterplot)
    g.add_legend()
    g.savefig("output.png")
    st.pyplot(g)
# box plot
    st.write("""### Bar Chart""")
    st.bar_chart(subdata)
    

# Line Chart
    st.write("""### Line Chart""")
    st.line_chart(subdata)

# Seperation of Dataset
    array = dataset.values
    X = array[:,0:3]
    Y = array[:,3]
    validatio_size = 0.20
    seed = 7
    X_train,X_validation,Y_train,Y_validation = model_selection.train_test_split(
        X,Y,test_size= validatio_size,random_state = seed)
    
# Test Harness
    scoring = 'accuracy'
    seed = 7

    chooseModel = st.selectbox("Choose a Model",("Logistic Regression","Linear Discriminant Analysis","K Neighbor Classifier"
    ,"Decision Tree Classifier","Gaussian NB","Support Vector Machine"))
    kFoldsplits = 10
    kfold = model_selection.KFold(n_splits = kFoldsplits, random_state = seed, shuffle=True)

    if chooseModel == "Logistic Regression":
        model = LogisticRegression()
        modelname = "Logistic Regression"
    elif chooseModel == "Linear Discriminant Analysis":
        model = LinearDiscriminantAnalysis()
        modelname = "Linear Discriminant Analysis"
    elif chooseModel == "K Neighbor Classifier":
        model = KNeighborsClassifier()
        modelname = "K Neighbor Classifier"
    elif chooseModel == "Decision Tree Classifier":
        model = DecisionTreeClassifier()
        modelname = "Decision Tree Classifier"
    elif chooseModel == "Gaussian NB":
        model = GaussianNB()
        modelname = "Gaussian NB"
    elif chooseModel == "Support Vector Machine":
        model = SVC()
        modelname = "Support Vector Machine"
    
    cv_results = model_selection.cross_val_score(model,X_train,Y_train, cv=kfold, scoring = scoring)

    st.text_area("Score of Cross Validation",cv_results.mean(),height=100)

    
    model.fit(X_train, Y_train)
    predictions = model.predict(X_validation)
    acc_score = accuracy_score(Y_validation, predictions)
    st.text_area("Accuracy of a Model",acc_score,height=100)
    st.text_area("Classification Report",classification_report(Y_validation, predictions),height=300)

    temperature = st.slider("Temperature", min_value=-20, max_value=50,value=10,step=1)
    humidity = st.slider("Humidity", min_value=1, max_value=99,value=30, step=1)
    air_pressure = st.slider("Air Pressure", min_value=900, max_value=1200, value=1000,step=10)

    ok = st.button("Predict Discomfort Index")
    

    if ok:
        #X = np.arrary([[temperature,humidity,air_pressure]])

        prediction = model.predict([[temperature,humidity,air_pressure]])
        if (prediction == "HIGH" or prediction=="high"):
            prediction = "Uncomfortable"
        elif (prediction == "MIDDLE" or prediction=="mid"):
            prediction = "So-So"
        elif (prediction == "LOW" or prediction=="low"):
            prediction = "Comfortable"
        else:
            return "error"
        #st.subheader("The estimated discomfort index is ${discomfort_index[0]}")
        st.write("Discomfort Index Below")
        st.subheader(prediction)



