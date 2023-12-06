import streamlit as st
import pickle
import pandas as pd
import os
import numpy as np
import altair as alt
import time

model = pickle.load(open('model_prediksi_asuransi.sav', 'rb'))

@st.cache_data()
def get_fvalue(val):    
    feature_dict = {"Male":1,"Female":0}    
    for key,value in feature_dict.items():        
        if val == key:            
            return value
def get_svalue(val):    
    feature_dict = {"Yes":1,"No":0}    
    for key,value in feature_dict.items():        
        if val == key:            
            return value
def get_rvalue(val):    
    feature_dict = {"southwest":1,"northwest":2,"southeast":3,"northeast":4}    
    for key,value in feature_dict.items():        
        if val == key:            
            return value
        
def get_value(val,my_dict):    
    for key,value in my_dict.items():        
        if val == key:            
            return value
        
app_mode = st.sidebar.selectbox('Select Page',['Home','Graph'])
if app_mode=='Home':
    st.title('INSURANCE PREDICTION')
    data = pd.read_csv('insurance.csv')
    age = st.number_input('Input Your Age', 0,100)
    sex = st.radio('Set Your Gender', ['Male','Female'])
    bmi = st.number_input('Set Your BMI', 20,50)
    child = st.number_input('Input Your Children Count', 0, 10)
    smoker = st.radio('Are You A Smoker', ['Yes','No'])
    region = st.radio('Select Your Region', ['Southwest','Northwest','Southeast','Northeast'])
    if st.button('Prediksi'):
        charges_pred = model.predict([[age, get_fvalue(sex), bmi, child, get_svalue(smoker), get_rvalue(region)]])
        charges_str = np.array(charges_pred)
        charges_float = float(charges_str[0])

        charges_formated = "{:.2f}".format(charges_float)
        bar = st.progress(100)
        for percent_complete in range(100):
            time.sleep(0.01)
            bar.progress(percent_complete + 1)
        time.sleep(1)
        st.write("HASIL PREDIKSI BIAYA ASURANSI: $",charges_formated)
elif app_mode == 'Graph': 
    data = pd.read_csv('insurance.csv')
    st.header('Dataset: ')
    st.write(data)
    st.header('RATA RATA BIAYA BERDASARKAN REGION')
    st.bar_chart(data['charges'].groupby(data.region).sum().sort_values(ascending = True))
    st.header('PERBANDINGAN BIAYA PEROKOK dan BUKAN PEROKOK')
    chart = alt.Chart(data).mark_circle().encode(
    x='smoker',
    y='charges',
    ).interactive()
    st.altair_chart(chart, theme="streamlit", use_container_width=True)
