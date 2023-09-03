import streamlit as st
import base64
import sklearn
import numpy as np
import pickle as pkl
from sklearn.preprocessing import MinMaxScaler
scal=MinMaxScaler()
#Load the saved model
model=pkl.load(open("final_model3.p","rb"))





st.set_page_config(page_title="Healthy Heart App",page_icon="⚕️",layout="centered",initial_sidebar_state="expanded")



def preprocess(age,sexP,cpP,trtbps,chol,fbsP,restecgP,thalachh,exngP,oldpeak,slpP,caa,thallP):   
    
    sex = 0
    # Pre-processing user input   
    if sexP=="male":
        sex=1 
    
    cp = 0
    if cpP=="Typical angina":
        cp=0
    elif cpP=="Atypical angina":
        cp=1
    elif cpP=="Non-anginal pain":
        cp=2
    elif cpP=="Asymptomatic":
        cp=3
       
    exng = 1
    if exngP=="Yes":
        exng=1
    elif exngP=="No":
        exng=0

    fbs = 1
    if fbsP=="Yes":
        fbs=1
    elif fbsP=="No":
        fbs=0
        
    slp = 1
    if slpP=="Upsloping: better heart rate with excercise(uncommon)":
        slp=0
    elif slpP=="Flatsloping: minimal change(typical healthy heart)":
          slp=1
    elif slpP=="Downsloping: signs of unhealthy heart":
        slp=2  
   
    thall = 0
    print('thallP ', thallP, type(thallP))
  
    restecg = 0
    if restecgP=="Nothing to note":
        restecg=0
    elif restecgP=="ST-T Wave abnormality":
        restecg=1
    elif restecgP=="Possible or definite left ventricular hypertrophy":
        restecg=2
     
    print('oldpeak ', type(oldpeak))
    print('thalachh ', type(thalachh))
    
    user_input=[float(age),float(sex),float(cp),float(trtbps),float(chol),float(fbs),float(restecg),float(thalachh),float(exng),float(oldpeak),float(slp),float(caa),float(thallP)]
    print('user_input ', user_input)
    user_input=np.array(user_input)
    user_input=user_input.reshape(1,-1)
    print('user_input reshaped ', user_input, ' ', type(user_input))
    
    prediction = model.predict(user_input)
    print(prediction)
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
sexP = st.radio("Select Gender: ", ('male', 'female'))
cpP = st.selectbox('Chest Pain Type',("Typical angina","Atypical angina","Non-anginal pain","Asymptomatic")) 
trtbps=st.selectbox('Resting Blood Sugar',range(1,500,1))
chol=st.selectbox('Serum Cholestoral in mg/dl',range(1,1000,1))
fbsP=st.radio("Fasting Blood Sugar higher than 120 mg/dl", ['Yes','No'])
restecgP=st.selectbox('Resting Electrocardiographic Results',("Nothing to note","ST-T Wave abnormality","Possible or definite left ventricular hypertrophy"))
thalachh=st.selectbox('Maximum Heart Rate Achieved',range(1,300,1))
exngP=st.selectbox('Exercise Induced Angina',["Yes","No"])
oldpeak=st.number_input('Oldpeak')
slpP = st.selectbox('Heart Rate Slope',("Upsloping: better heart rate with excercise(uncommon)","Flatsloping: minimal change(typical healthy heart)","Downsloping: signs of unhealthy heart"))
caa=st.selectbox('Number of Major Vessels Colored by Flourosopy',range(0,4,1))
thallP=st.selectbox('Thalium Stress Result',range(0,4,1))

pred = preprocess(age,sexP,cpP,trtbps,chol,fbsP,restecgP,thalachh,exngP,oldpeak,slpP,caa,thallP)

st.write(pred)


if st.button("Predict"):
  
  if pred[0] == 1:
    st.error('Warning! You have high risk of getting a heart attack!')
    
  else:
    st.success('You have lower risk of getting a heart disease!')
    
