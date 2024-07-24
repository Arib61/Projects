import numpy as np
import pickle
import streamlit as st

# Load the model
loaded_model = pickle.load(open("C:/Machine_learning Python/projets/diabetDeployment/trained_model.sav", 'rb'))

#Crearion de la fonction de la prediction
def predictionF(input_data):
    # Convert input data to numpy array
    input_data_numpy = np.asarray(input_data, dtype=float)
    # Reshape the array
    input_data_reshaped = input_data_numpy.reshape(1, -1)
    # Make a prediction
    prediction = loaded_model.predict(input_data_reshaped)
    # Return a message based on the prediction
    if prediction[0] == 1:
        return "The person is diabetic."
    else:
        return "The person is not diabetic."

#La fonction principal main 
def main():
    # Title of the app 
    st.title('Diabetes Prediction Web App')

    # Getting user input
    #Les different argument de note application

    Pregnancies = st.text_input('Number of Pregnancies')
    Glucose = st.text_input('Glucose Level')
    BloodPressure = st.text_input('Blood Pressure Value')
    SkinThickness = st.text_input('Skin Thickness Value')
    Insulin = st.text_input('Insulin Level')
    BMI = st.text_input('BMI Value')
    DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function Value')
    Age = st.text_input('Age')

    # Apres le clique sur la bouton test Result
    if st.button('Diabetes Test Result'):
        # Convert inputs to float
        # Enter nos arguments dans le tableau input_data
        try:
            input_data = [
                float(Pregnancies),
                float(Glucose),
                float(BloodPressure),
                float(SkinThickness),
                float(Insulin),
                float(BMI),
                float(DiabetesPedigreeFunction),
                float(Age),
            ]
            # Get the prediction
            #Stocker le resultat de la prediction dans une variable result
            result = predictionF(input_data)
            st.success(result)
        except ValueError:
            st.error("Please enter valid numbers.")

# Run the app (demarer notre application)
if __name__ == '__main__':
    main()
#Pour le demarrage:

#cd C:\Machine_learning Python\projets\diabetDeployment
#streamlit run diabet_app.py

