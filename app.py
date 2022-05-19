import numpy as np
import pandas as pd
import streamlit as st
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn import metrics
import pickle as pkl
from PIL import Image

st.set_page_config(layout="wide")

st.markdown("<h1 style='text-align: center; color:#42D1C6; font-size:50px;'>--HEART DISEASE PREDICTION--</h1>",unsafe_allow_html=True)
st.markdown("""<style>.font {font-size:25px;text-align: center;}</style>""", unsafe_allow_html=True)
st.markdown('<p class="font">This web app aims to help you find out whether you are at a risk of developing a heart disease or not.</p>', unsafe_allow_html=True)

#st.image('heart1.jpg',width=350)
background = Image.open("heart1.jpg")
col1, col2, col3 = st.columns([2, 3, 2])
col2.image(background,width=350)

def main_func():
    st.sidebar.info("Please select the required fields below!")
    age = st.sidebar.slider("Age", 21, 81, 23)
    sex = st.sidebar.radio("Gender (1=Male, 0=Female)", ["1", "0"])
    cp = st.sidebar.selectbox(
        "Chest pain (0=Typical angina, 1=Atypical angina, 2=Non—anginal pain, 3=Asymptotic)", ["0", "1", "2", "3"])
    trestbps = st.sidebar.slider("Resting blood pressure", 100, 400, 110)
    chol = st.sidebar.slider("chol", 100, 400, 110)
    fbs = st.sidebar.radio(
        "Fasting blood sugar (1=fbs>120mg/dl, 0=fbs<120 mg/dl)", ["1", "0"])
    restecg = st.sidebar.selectbox(
        "Resting ECG (0=Normal ,1=Having ST-T wave abnormality, 2=Left ventricular hyperthrophy)", ["0", "1", "2"])
    thalach = st.sidebar.slider("maximum heart rate achieved", 100, 200, 110)
    exang = st.sidebar.radio(
        "Exercise induced angina(1=Yes, 0=No)", ["1", "0"])
    oldpeak = st.sidebar.slider(
        "ST depression induced by exercise relative to rest", 0.0, 5.0, 0.5)
    slope = st.sidebar.radio(
        "The slope of the peak exercise ST segment (0=Upsloping, 1=Flatsloping, 2=Downsloping)", ["0", "1", "2"])
    ca = st.sidebar.slider(
        "Number of major vessels (0-3) colored by flourosopy", 0, 3, 1)
    thal = st.sidebar.radio(
        "Thal (0 = normal; 1 = fixed defect; 2 = reversable defect)",["0", "1", "2"])
    data = {
        'age': age,
        'sex': sex,
        'cp': cp,
        'trestbps': trestbps,
        'chol': chol,
        'fbs': fbs,
        'restecg': restecg,
        'thalach': thalach,
        'exang': exang,
        'oldpeak': oldpeak,
        'slope': slope,
        'ca': ca,
        'thal': thal
    }
    features = pd.DataFrame(data, index=[0])
    return features


df = main_func()
heart_raw = pd.read_csv("heart_cleveland_upload.csv")

standardScaler = StandardScaler()
feat=['age','sex','cp','trestbps','chol','fbs','restecg','thalach' ,'exang','oldpeak','slope','ca','thal']
heart_raw[feat] = standardScaler.fit_transform(heart_raw[feat])

X = heart_raw.drop(['condition'], axis=1)
Y = heart_raw.condition
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2,random_state=1)

for i in range(1, 20):
    knn2 = KNeighborsClassifier(n_neighbors=i)  # n_neighbors means k
    knn2.fit(x_train, y_train)

prediction1 = knn2.predict(x_test)
print("{} - KNN Score: {:.2f}%".format(2, knn2.score(x_test, y_test) * 100))

prediction = knn2.predict(df)
if prediction[0] == 0:
    st.error('Warning! You have high risk of getting a heart attack!')
else:
    st.success('You have lower risk of getting a heart disease!')
               
st.info("Caution: This is just a machine learning prediction program and not doctoral advice. Kindly see a doctor if you feel the symptoms persist.")
