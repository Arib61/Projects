import numpy as np
import pickle
import streamlit as st



load_model = pickle.load(open('C:/Machine_learning Python/projets/obesityPrediction/obesity_model.sav' , 'rb'))



def  prediction_obesity(input_data):
    #Input the data into the numpy array:
    input_dataNumpuy = np.asarray(input_data)
    #Reshape the data:
    input_dataReshaped = input_dataNumpuy.reshape(1,-1)
    prediction = load_model.predict(input_dataReshaped)
    print(prediction[0])
    obs = prediction[0]
    if obs == 1:
        test = 'Normal weight'
    elif obs == 2:
        test = 'Overweight'
    if obs == 3:
        test = 'Obese'
    if obs == 4:
        test = 'Underweight'
    print("Your obesity is: ", test)
    return test


def main():
    st.title('Obesity test Web APP')
    Gender = st.text_input("Enter your gender (1: male, 0: female): ")
    Age = st.text_input("Enter your age: ")
    Height = st.text_input("Enter your height: ")
    Weight = st.text_input("Enter your weight: ")
    BMI = st.text_input("Enter the BMI : (entre 18 à 25)")
    PhysicalActivityLevel = st.text_input("Enter your physical activity level : (entre 1 à 5)")

    test = ''
    if st.button('Calories Test Result'):
        test =  prediction_obesity([Age,Gender,Height,Weight,BMI,PhysicalActivityLevel])
        st.success(test)


if (__name__ == '__main__') :
    main()