import streamlit as st
import base64
import sklearn
import numpy as np
import pickle as pkl
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow import keras
scal=MinMaxScaler()
#Load the saved model

model = tf.keras.models.load_model('final_model.h5')



st.set_page_config(page_title="Stroke prediction app ",page_icon="smiley",layout="centered",initial_sidebar_state="expanded")



def preprocess(gender,age,hypertension,alcohol_take,heart_disease,residence_type,avg_glucose_level,bmi,smoking_status ):   
 
    
    # Pre-processing user input   
    if gender=="male":
        gender=1 
    else: gender=0
	
    if heart_disease =="Yes":
        heart_disease = 1
    else:
        heart_disease = 0
    
    
    if residence_type=="Urban":
        residence_type=1
    else: residence_type = 0
	
    
    if smoking_status=="formely smoked":
        smoking_status = 1
    elif smoking_status=="never smoked":
        smoking_status = 2
    else:
        smoking_status =3
	
	


    user_input=[gender,age,hypertension,alcohol_take,residence_type,avg_glucose_level,bmi,smoking_status]
    user_input=np.array(user_input)
    user_input=user_input.reshape(1,-1)
    user_input=scal.fit_transform(user_input)
    prediction = model.predict(user_input)

    return prediction

    

       
    # front end elements of the web page 
html_temp = """ 
    <div style ="background-color:pink;padding:13px"> 
    <h1 style ="color:black;text-align:center;">Stroke Prediction App</h1> 
    </div> 
    """
      
# display the front end aspect
st.markdown(html_temp, unsafe_allow_html = True) 
st.subheader('by leesa-menezes ')
      
# following lines create boxes in which user can enter data required to make prediction
gender= st.radio("Select Gender: ", ('male', 'female'))
age=st.text_input("Age","Enter here")
hypertension =st.text_input("Hypertension","Enter here")
alcohol_take = st.text_input("Alcohol intake", "Please enter the amount of glasses consumed daily")
heart_disease= st.radio("Select you have a heart disease or not: ", ('Yes', 'No'))
residence_type= st.radio("Select your Residence Type: ", ('Urban', 'Rural'))
avg_glucose_level=st.text_input("Average Glucose Level","Please enter your value here")
bmi=st.text_input("BMI","Enter here")
smoking_status= st.radio("Select your smoking status: ", ('formely smoked', 'never smoked', 'smokes'))


#user_input=preprocess(sex,cp,exang, fbs, slope, thal )
pred=preprocess(gender,age,hypertension,alcohol_take,heart_disease,residence_type,avg_glucose_level,bmi,smoking_status)

output = np.argmax(pred[0])


if st.button("Predict"):    
  if output == 1:
    st.error('Warning! You have high risk of getting a stroke!')
    
  else:
    st.success('You have lower risk of getting a stroke!')
    
   



st.sidebar.subheader("About App")

st.sidebar.info("This web app is helps you to find out whether you are at a risk of developing a heart disease.")
st.sidebar.info("Enter the required fields and click on the 'Predict' button to check whether you have a healthy heart")
st.sidebar.info("Don't forget to rate this app")



feedback = st.sidebar.slider('How much would you rate this app?',min_value=0,max_value=5,step=1)

if feedback:
  st.header("Thank you for rating the app!")
  st.info("Caution: This is just a prediction and not doctoral advice. Kindly see a doctor if you feel the symptoms persist.")
