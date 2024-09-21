import streamlit as st
import requests
import json

# Function to validate input
def validate_input(data):
    for key, value in data.items():
        if value is None:
            return False, f"Please provide a valid input for {key}."
        if isinstance(value, (int, float)) and value < 0:
            return False, f"Value for {key} cannot be negative."
    return True, ""

# Function to call Flask API
def get_prediction(data):
    url = "https://heart-failure-predictor-model-2.onrender.com/predict"  # Update with the correct host if deployed remotely
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    return response.json()

# Initialize session state for navigation
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Navigation buttons
if st.session_state.page == 'home':
    # Home Page Content
    st.title("Welcome to the Heart Failure Prediction App")
    st.write("""
        This is an app that predicts the likelihood of heart failure based on clinical data.
        Click the button below to input data and get a prediction.
    """)
    

    if st.button("Go to Heart Failure Prediction"):
        st.session_state.page = 'prediction'
        st.stop()

elif st.session_state.page == 'prediction':
    # Prediction Page Content
    st.title("Heart Failure Prediction")

    # Form inputs for prediction
    age = st.number_input('Age', min_value=1)
    
    anaemia_option = st.selectbox('Anaemia (Yes/No)', ['No', 'Yes'])
    anaemia = 1 if anaemia_option == 'Yes' else 0 

    sex_option = st.selectbox('Sex (Male/Female)', ['Female', 'Male'])
    sex = 1 if sex_option == 'Male' else 0

    if sex_option == 'Male':
        st.write("You selected Male")
        creatinine_phosphokinase = st.number_input('Creatinine Phosphokinase (Normal: 38 to 174 mcg/L)', min_value=0, max_value=200)
    else:
        st.write("You selected Female")
        creatinine_phosphokinase = st.number_input('Creatinine Phosphokinase (Normal: 26 to 140 mcg/L)', min_value=0, max_value=200)

    diabetes_option = st.selectbox('Diabetes (Yes/No)', ['No', 'Yes'])
    diabetes = 1 if diabetes_option == 'Yes' else 0
    
    ejection_fraction = st.number_input('Ejection Fraction (Normal: 55-70 %)', min_value=0)
    
    high_blood_pressure_option = st.selectbox('High Blood Pressure (Yes/No)', ['No', 'Yes'])
    high_blood_pressure = 1 if high_blood_pressure_option == 'Yes' else 0
    
    platelets = st.number_input('Platelets (k/mL)', min_value=0)
    
    serum_creatinine = st.number_input('Serum Creatinine (Normal: 0.6-1.2 mg/dL)', min_value=0.0, format="%.2f")
    
    serum_sodium = st.number_input('Serum Sodium (Normal: 135-145 mEq/L)', min_value=0)
    
    smoking_option = st.selectbox('Smoking (Yes/No)', ['No', 'Yes'])
    smoking = 1 if smoking_option == 'Yes' else 0
    
    time = st.number_input('Follow-up period (days)', min_value=0)

    # Prepare data
    input_data = {
        "age": age,
        "anaemia": anaemia,
        "creatininePhosphokinase": creatinine_phosphokinase,
        "diabetes": diabetes,
        "ejectionFraction": ejection_fraction,
        "highBloodPressure": high_blood_pressure,
        "platelets": platelets,
        "serumCreatinine": serum_creatinine,
        "serumSodium": serum_sodium,
        "sex": sex,
        "smoking": smoking,
        "time": time
    }

    if st.button("Predict"):
        # Call the prediction API
        with st.spinner('Predicting...'):
            try:
                prediction = get_prediction(input_data)
                if prediction['prediction'] == 'Death Event':
                    st.warning("Prediction: There is a chance that you will have heart failure.")
                else:
                    st.success("Prediction: You're in good health!")
            except requests.exceptions.RequestException as e:
                st.error(f"Error calling the API: {e}")

    if st.button("Back to Home"):
        st.session_state.page = 'home'
        st.stop()
