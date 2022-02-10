import streamlit as st
import pandas as pd
import matplotlib 
import seaborn as sns
import pickle
import mysql.connector
import pandas as pd

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



def show_explore_page():
    st.title("Visualize Data")
    st.write("""### Visualize Aqara THP Data or KMA Data""")
    chooseDB = st.selectbox("Aqara DB or KMA DB",("KMA DB","Aqara DB"))
    choosePlot=st.selectbox("Correlation chart, bar chart or data frame",("Correlation","Bar Chart", "Data Frame"))
    if chooseDB == "KMA DB":
            dataset = datasetKMA
            subdata = subdataKMA
    elif chooseDB == "Aqara DB":
            dataset = datasetAqara
            subdata = subdataAqara

    if choosePlot == "Correlation":
        st.write("""### Pair Grid Chart for Correlation""")
        g = sns.PairGrid(dataset, hue="class")
        g.map_diag(sns.histplot)
        g.map_offdiag(sns.scatterplot)
        g.add_legend()
        g.savefig("output.png")
        st.pyplot(g)
    elif choosePlot == "Bar Chart":
        st.write("""### Bar Chart""")
        st.bar_chart(subdata)
    elif choosePlot == "Data Frame":
        test=st.text_area("Dataset Head",pd.DataFrame.to_string(dataset),height=150)

    # 데이터 
# box plot
 #   boxplot = dataset.plot(kind='box', subplots=True, layout=(2,2), sharex=False, sharey=False)
 #   st.pyplot(boxplot)

# histogram
 #   histogram=dataset.hist()
 #   st.pyplot(histogram)

# scatter plot matrix
  #  scatter= sns.scatterplot(x="temperature",y="humidity",data=dataset)
   # st.pyplot(scatter)
