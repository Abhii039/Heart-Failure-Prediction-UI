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
    st.image("data:image/jpeg;base64,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")
    

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
    
    ejection_fraction = st.number_input('Ejection Fraction (Normal: 55-70 %)', min_value=0, max_value=100)
    
    high_blood_pressure_option = st.selectbox('High Blood Pressure (Yes/No)', ['No', 'Yes'])
    high_blood_pressure = 1 if high_blood_pressure_option == 'Yes' else 0
    
    platelets = st.number_input('Platelets (k/mL)', min_value=0 ,max_value=500000)
    

    serum_creatinine = st.number_input('Serum Creatinine (Normal: 0.6-1.2 mg/dL)', min_value=0.0, max_value=2.0,format="%.2f")
    
    serum_sodium = st.number_input('Serum Sodium (Normal: 135-145 mEq/L)', min_value=0 , max_value=200)
    
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
