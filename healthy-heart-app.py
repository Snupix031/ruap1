import streamlit as st
import base64
import sklearn
import numpy as np
import pickle as pkl
from sklearn.preprocessing import MinMaxScaler
scal=MinMaxScaler()
#Load the saved model
model=pkl.load(open("final_model.p","rb"))





st.set_page_config(page_title="Healthy Heart App",page_icon="⚕️",layout="centered",initial_sidebar_state="expanded")



def preprocess(age,sex,cp,trtbps,restecg,chol,fbs,thalachh,exng,oldpeak,slp,caa,thall):   
 
  
    # Pre-processing user input   
    if sex=="male":
        sex=1 
    else: sex=0
    
    
    if cp=="Typical angina":
        cp=0
    elif cp=="Atypical angina":
        cp=1
    elif cp=="Non-anginal pain":
        cp=2
    elif cp=="Asymptomatic":
        cp=3
       
    if exng=="Yes":
        exng=1
    elif exng=="No":
        exng=0
    
    if fbs=="Yes":
        fbs=1
    elif fbs=="No":
        fbs=0
   
    if slp=="Upsloping: better heart rate with excercise(uncommon)":
        slp=0
    elif slp=="Flatsloping: minimal change(typical healthy heart)":
          slp=1
    elif slp=="Downsloping: signs of unhealthy heart":
        slp=2  
   
    if thall==" null":
        thall=0
    elif thall=="fixed defect":
        thall=1
    elif thall=="normal":
        thall=2
    elif thall=="reversable defect":
        thall=3
  
    if restecg=="Nothing to note":
        restecg=0
    elif restecg=="ST-T Wave abnormality":
        restecg=1
    elif restecg=="Possible or definite left ventricular hypertrophy":
        restecg=2
     

    user_input=[age,sex,cp,trtbps,restecg,chol,fbs,thalachh,exng,oldpeak,slp,caa,thall]
    user_input=np.array(user_input)
    user_input=user_input.reshape(1,-1)
    #user_input=scal.fit_transform(user_input)
    prediction = model.predict(user_input)
   
    return  prediction
       
    # front end elements of the web page 
html_temp = """ 
    <div style ="background-color:pink;padding:13px"> 
    <h1 style ="color:black;text-align:center;">Healthy Heart App</h1> 
    </div> 
    """
      
# display the front end aspect
st.markdown(html_temp, unsafe_allow_html = True) 

      
# following lines create boxes in which user can enter data required to make prediction
age=st.selectbox ("Age",range(1,121,1))
sex = st.radio("Select Gender: ", ('male', 'female'))
cp = st.selectbox('Chest Pain Type',("Typical angina","Atypical angina","Non-anginal pain","Asymptomatic")) 
trtbps=st.selectbox('Resting Blood Sugar',range(1,500,1))
chol=st.selectbox('Serum Cholestoral in mg/dl',range(1,1000,1))
fbs=st.radio("Fasting Blood Sugar higher than 120 mg/dl", ['Yes','No'])
restecg=st.selectbox('Resting Electrocardiographic Results',("Nothing to note","ST-T Wave abnormality","Possible or definite left ventricular hypertrophy"))
thalachh=st.selectbox('Maximum Heart Rate Achieved',range(1,300,1))
exng=st.selectbox('Exercise Induced Angina',["Yes","No"])
oldpeak=st.number_input('Oldpeak')
slp = st.selectbox('Heart Rate Slope',("Upsloping: better heart rate with excercise(uncommon)","Flatsloping: minimal change(typical healthy heart)","Downsloping: signs of unhealthy heart"))
caa=st.selectbox('Number of Major Vessels Colored by Flourosopy',range(0,4,1))
thall=st.selectbox('Thalium Stress Result',range(0,4,1))



pred=preprocess(age,sex,cp,trtbps,restecg,chol,fbs,thalachh,exng,oldpeak,slp,caa,thall)

st.write(pred)


if st.button("Predict"):    
  if pred[0] == 1:
    st.error('Warning! You have high risk of getting a heart attack!')
    
  else:
    st.success('You have lower risk of getting a heart disease!')
    
