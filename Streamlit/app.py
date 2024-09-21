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
    url = "http://127.0.0.1:10000/predict"  # Update with the correct host if deployed remotely
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    return response.json()

# Multi-page navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select Page", ["Home", "Heart Failure Prediction"])

if page == "Home":
    # Home Page Content
    st.title("Welcome to the Heart Failure Prediction App")
    st.write("""
        This is an app that predicts the likelihood of heart failure based on clinical data.
        Navigate to the "Heart Failure Prediction" page to input data and get a prediction.
    """)
    st.image("https://cdn.pixabay.com/photo/2015/07/05/13/44/heart-832533_1280.jpg", use_column_width=True)

elif page == "Heart Failure Prediction":
    # Prediction Page Content
    st.title("Heart Failure Prediction")

    # Form inputs for prediction
    age = st.number_input('Age', min_value=0.0, format="%.1f")
    anaemia = st.selectbox('Anaemia (1 = Yes, 0 = No)', [0, 1])
    creatinine_phosphokinase = st.number_input('Creatinine Phosphokinase (mcg/L)', min_value=0.0)
    diabetes = st.selectbox('Diabetes (1 = Yes, 0 = No)', [0, 1])
    ejection_fraction = st.number_input('Ejection Fraction (%)', min_value=0.0, format="%.1f")
    high_blood_pressure = st.selectbox('High Blood Pressure (1 = Yes, 0 = No)', [0, 1])
    platelets = st.number_input('Platelets (k/mL)', min_value=0.0, format="%.1f")
    serum_creatinine = st.number_input('Serum Creatinine (mg/dL)', min_value=0.0, format="%.2f")
    serum_sodium = st.number_input('Serum Sodium (mEq/L)', min_value=0.0, format="%.1f")
    sex = st.selectbox('Sex (1 = Male, 0 = Female)', [0, 1])
    smoking = st.selectbox('Smoking (1 = Yes, 0 = No)', [0, 1])
    time = st.number_input('Follow-up period (days)', min_value=0.0, format="%.1f")

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

    # Validate input and show prediction button
    if st.button("Predict"):
        is_valid, validation_message = validate_input(input_data)
        
        if is_valid:
            # Call the prediction API
            with st.spinner('Predicting...'):
                try:
                    prediction = get_prediction(input_data)
                    st.success(f"Prediction: {prediction['prediction']}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error calling the API: {e}")
        else:
            st.error(validation_message)
