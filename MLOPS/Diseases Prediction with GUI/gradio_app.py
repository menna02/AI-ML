import pickle
import gradio as gr

def load_models():
    diabetes_model = pickle.load(open('Saved Models/diabetes_model.sav','rb'))
    heart_model = pickle.load(open('Saved Models/heart_disease_model.sav','rb'))
    parkinsons_model = pickle.load(open('Saved Models/parkinsons_model.sav', 'rb'))

    return diabetes_model, heart_model, parkinsons_model

def get_prediction(model, input_data):
    pred = model.predict([input_data])
    return pred[0]

diabetes_model, heart_model, parkinsons_model = load_models()

def predict_diabetes(pregnances, skin, Pedigree, glucose, insulin, age, blood, bmi):
    input_data = [pregnances, skin, Pedigree, glucose, insulin, age, blood, bmi]
    pred = get_prediction(diabetes_model, input_data)

    if pred==0:
        return 'Not Diabetic'
    else:
        return 'Diabetic'

diabetic_interface = gr.Interface(
    fn=predict_diabetes,
    inputs=[
        gr.Number(label='Pregnances'),
        gr.Number(label='Skin Thickness'),
        gr.Number(label='Pedigree'),
        gr.Number(label='Glucose Level'),
        gr.Number(label='Insulin Level'),
        gr.Number(label='Age'),
        gr.Number(label='Blood Pressure'),
        gr.Number(label='BMI')
    ],
    outputs='text',
    title='Diabetes Disease Prediction'
).launch(share=True)


