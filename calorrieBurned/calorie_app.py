import numpy as np
import pickle
import streamlit as st



load_model = pickle.load(open('C:/Machine_learning Python/projets/calorrieBurned/calorie_model.sav','rb'))
print(load_model)

def  prediction_calories(input_data):
    #Input the data into the numpy array:
    input_dataNumpuy = np.asarray(input_data)
    #Reshape the data:
    input_dataReshaped = input_dataNumpuy.reshape(1,-1)
    prediction = load_model.predict(input_dataReshaped)
    return prediction[0]


def main():
    st.title('Burning Calories Web APP')

    Gender = st.text_input("Enter your gender (1: male, 0: female): ")
    Age = st.text_input("Enter your age: ")
    Height = st.text_input("Enter your height: ")
    Weight = st.text_input("Enter your weight: ")
    Duration = st.text_input("Enter the test duration (min): ")
    Heart_Rate = st.text_input("Enter your heart rate: ")
    Body_Temp = st.text_input("Enter your body temperature (C): ")


    diagnostics = ''

    if st.button('Calories Test Result'):
        diagnostics =  prediction_calories([Gender,Age,Height,Weight,Duration,Heart_Rate,Body_Temp])

    
    st.success(diagnostics)


if (__name__ == '__main__') :
    main()
