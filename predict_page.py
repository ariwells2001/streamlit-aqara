import streamlit as st
import pickle
import numpy as np

def load_model():
    with open('aqara.sav','rb') as file:
        data = pickle.load(file)
    return data

def load_modelKMA():
    with open('KMA.sav','rb') as file:
        dataKMA = pickle.load(file)
    return dataKMA



def show_predict_page():
    st.title("Discomfort Index Prediction")
    
    st.write("""### Trained From Aqara DB or KMA DB""")
    chooseDB = st.selectbox("Aqara DB or KMA DB",("KMA DB","Aqara DB"))

    if chooseDB == "KMA DB":
            model = load_modelKMA()
    elif chooseDB == "Aqara DB":
            model = load_model()

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


        
        
    

     
