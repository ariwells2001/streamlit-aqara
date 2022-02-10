import streamlit as st
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

from tpot import TPOTRegressor
from tpot import TPOTClassifier

from sklearn.model_selection import train_test_split
from sklearn import metrics


def show_autoML_page():
    def auto_tpot(data,target_col,predict_type, tr_size=0.7,ts_size=0.3, random_state=1123, file_name = "temp.py"):
    
        X_train, X_test, y_train, y_test = train_test_split(data, target,
                                                       train_size = tr_size , test_size = ts_size, random_state=42)
    
        if predict_type == 'Regressor':
            tpot = TPOTRegressor(generations=5, population_size=50, verbosity=0)
        elif predict_type == 'Classifier':
            tpot = TPOTClassifier(generations=5, population_size=50, verbosity=0)
        else :
            print("predict type must be 'regressor' or 'classifier'")

        tpot.fit(X_train, y_train)
    
        df_temp = pd.DataFrame(dict(tpot.evaluated_individuals_.items())).T
        df_temp.reset_index(inplace=True)
        df_temp["model"] = list(map(lambda x : x.split("(")[0], df_temp['index']))
        df_temp.rename(columns={'index':'parameters'},inplace=True)
        result = df_temp[['model','internal_cv_score','parameters']].sort_values(by='internal_cv_score',ascending = False).reset_index().drop(['index'],axis=1).head(100)
        return X_test,y_test, tpot, result


    st.title('최적의 머신러닝 알고리즘 자동 생성기')
    st.write("Auto ML & Streamlit for Aqara")
    #st.header('최적의 머신러닝 알고리즘 찾기')

    uploaded_file = st.file_uploader("파일을 선택하세요.")

    if uploaded_file is not None:
        df_pred = pd.read_csv(uploaded_file,encoding='utf-8-sig')
        st.write(df_pred)
    
        try:
            target_col  = st.selectbox("Target",tuple(df_pred.columns))
            predict_type  = st.selectbox("머신러닝 종류",('Regressor', 'Classifier'))
            
        except:
            st.error("Target column and Predict type is required!")
        eda_col  = st.selectbox("Predictor",tuple(df_pred.columns))
    

    if st.button("최적알고리즘생성"):
        data = df_pred.drop([target_col],axis=1)
        target = df_pred[target_col]
        try:
            df_dtype = pd.DataFrame(data.dtypes,columns=["Dtype"])

            cat_cols = list(df_dtype[df_dtype.Dtype == 'object'].index) #categorical columns
            num_cols = list(df_dtype[df_dtype.Dtype != 'object'].index) #numerical columns

            cat_data = data[cat_cols]
            cat_dummy = pd.get_dummies(cat_data)

            data_dummy = pd.concat([cat_dummy,data[num_cols]],axis=1)
            data_dummy = (data_dummy-data_dummy.min())/data_dummy.max()
            data = pd.concat([data_dummy,target],axis=1)
        except:
            pass

        if uploaded_file is not None:
            with st.spinner('몇분만 기다리세요...'):

                    X_test,y_test, tpot, result = auto_tpot(data, target_col,predict_type, tr_size=0.7,ts_size=0.3, random_state=123)
                    st.write(result)
                    preds = tpot.predict(X_test)
                
                    if predict_type == 'Classifier':
                        score = metrics.accuracy_score(preds,y_test)
                    else:
                        score = metrics.r2_score(preds,y_test)
                
                    st.write('Best Model, Scored Internal CV score {}.'.format(score))
                    st.write("Code to produce the Best Model is below")
                    st.code(tpot.export())
