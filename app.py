import streamlit as st
import os
import database as db
from keras.models import model_from_json
import numpy as np
import gdown
from tensorflow.keras.utils import img_to_array
from tensorflow.keras.preprocessing import image
if os.path.exists('my_model_weights.h5'):
    pass
else:
    weight_url = "https://drive.google.com/file/d/1ru5-7k_oa4hrEmQOEuVD5ByuHWdv3BUT/view?usp=sharing"
    gdown.download(weight_url, 'my_model_weights.h5', quiet=False,fuzzy=True)
if os.path.exists('model_arch.json'):
    pass
else:
    json_url = "https://drive.google.com/file/d/1osy1hCGoDgI25MPd88omZZHGASJS1_6Q/view?usp=sharing"
    gdown.download(json_url, 'model_arch.json', quiet=False,fuzzy=True)
with open('model_arch.json', 'r') as json_file:
    json_savedModel= json_file.read()
model = model_from_json(json_savedModel)
model.load_weights('my_model_weights.h5')


def form():
    st.title ("Form")
    with st.form(key= "Information form"):
        col1, col2 = st.columns(2)
        with col1:
            st.title('Doctor Information')
            docname=st.text_input("Enter Doctor name ")
            doc_contact=st.number_input("Enter Doctor contact number ",step=1)
            doc_quli=st.text_input("Enter Doctor Qualification ")
            hospital_name=st.text_input("Enter Hospital name ")
            hospital_address=st.text_input("Enter Hospital Address ")
        with col2:
            st.title('Patient Information')
            id=st.text_input("Enter Patient id: ")
            name=st.text_input("Enter Patient name ")
            age=st.number_input("Enter Patient age: ",step=1)
            date = st.date_input("Enter the date: ")
            address=st.text_input("Enter Patient Address: ")
            pat_contact=st.number_input("Enter Patient contact number: ",step=1)
            aadhar=st.number_input("Enter Patient aadhar number: ",step=1)
            remark=st.text_input("Enter Remark (for Doctor Use): ")
            st.markdown("Predicted Class is "+str(pred_class))
            pred=str(pred_class)
        submission=st.form_submit_button(label="Submit")
        
        if submission == True :
            db.insert_result(docname,doc_contact,doc_quli,hospital_name,hospital_address,id,name,age,date,address,pat_contact,aadhar,remark,pred)
            st.success ("Successfully submitted")
            
            st.title('Results')
            st.markdown('Patient id: '+str(id))
            st.markdown('Name: '+name)
            st.markdown('Age: '+str(age))
            st.markdown('Date: '+str(date))
            st.markdown('Address: '+address)
            st.markdown('Contact: '+str(pat_contact))
            st.markdown('Aadhar: '+str(aadhar))
            st.markdown('Prediction : '+pred)


def predict_img(img):
    img = img_to_array(img)/255
    img = np.expand_dims(img, axis=0)
    result = model.predict(img)
    result = np.argmax(result, axis=-1)
    target_names = ["Normal","Viral Pneumonia","COVID-19"]
    return target_names[result[0]]

html_temp = """
    <div style="background-color:#2F3C7E;padding:10px;margin-bottom: 25px">
    <h2 style="color:white;text-align:center;">COVID-19 Detection</h2>
    <p style="color:white;text-align:center;" >This is a <b>CovScan</b> tool used for prediction of the <b> COVID-19</b>.</p>
    </div>
    """
st.markdown(html_temp,unsafe_allow_html=True)

option = st.radio('', ['Choose a test image', 'Choose your own image'])
if option == 'Choose your own image':
    uploaded_file = st.file_uploader("Choose an image...", type="jpg") #file upload
    if uploaded_file is not None:
        
        img = image.load_img(uploaded_file, target_size=(224,224,3))
        pred_class = predict_img(img)
        col1, col2 = st.columns(2)
        with col1:
            st.image(img, width=200)
        with col2:
            st.success("Predicted :  [" + str(pred_class) + "] ")
        form()
else:
    test_images = os.listdir('sample_images')
    test_image = st.selectbox('Please select a test image:', test_images)
    file_path = 'sample_images/' + test_image
    img = image.load_img(file_path, target_size=(224,224,3))
    pred_class = predict_img(img)
    col1, col2 = st.columns(2)
    with col1:
        st.image(img, width=200)
    with col2:
        st.success("Predicted :  [" + str(pred_class) + "] ")
    form()
