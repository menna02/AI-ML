import pickle
import streamlit as st
from streamlit_option_menu import option_menu

def load_models():
    diabetes_model = pickle.load(open('Saved Models/diabetes_model.sav','rb'))
    heart_model = pickle.load(open('Saved Models/heart_disease_model.sav','rb'))
    parkinsons_model = pickle.load(open('Saved Models/parkinsons_model.sav', 'rb'))

    return diabetes_model, heart_model, parkinsons_model

def get_diabetes_input():
    col1, col2, col3 = st.columns(3)

    with col1:
        pregnances = int(st.text_input('Number of Pregnancies', 0))
        skin = int(st.text_input('Skin Thinkness Value', 0))
        Pedigree = int(st.text_input('Diabetes Pedigree Function Value', 0))

    with col2:
        glucose = int(st.text_input('Glucose Level', 0))
        insulin = int(st.text_input('Insulin Level', 0))
        age = int(st.text_input('Age',0))

    with col3:
        blood = int(st.text_input('Blood Pressure Value',0))
        bmi = int(st.text_input('Body Mass Index Value',0))
    
    return pregnances, skin, Pedigree, glucose, insulin, age, blood, bmi

def get_prediction(model, input_data):
    pred = model.predict([input_data])
    return pred[0]

def main():
    diabetes_model, heart_model, parkinsons_model = load_models()
    with st.sidebar:
        selected = option_menu('Multiple Diseases Prediction', ['Diabetes Prediction', 'Heart Disease Prediction', 'Parkinsons Prediction'],
                               icons=['activity', 'heart', 'person'], default_index = 0)
        
    if selected=='Diabetes Prediction':
        st.title('Diabetes Prediction using ML')
        input_data = get_diabetes_input()
        if input_data and st.button('Show Result'):
            pred = get_prediction(diabetes_model, input_data)
            if pred==1:
                st.success('The person is diabetic')
            else:
                st.success('The person is not diabetic')


if __name__=='__main__':
    main()

