import streamlit==1.41.1 as st
import numpy as np
import joblib
import requests

# Load the model
model = joblib.load('crop_yield_production_model.pkl')

# Function to make predictions
def predict_crop_yield(input_data):
    # Convert to numpy array and reshape for prediction
    input_data = np.array(input_data).reshape(1, -1)
    
    # Make prediction
    prediction = float(model.predict(input_data)[0])
    return prediction

# Streamlit interface
def main():
    st.title("Crop Yield Prediction")
    
    # Form to input data
    with st.form(key="yield_form"):
        region = st.selectbox("Region", ["North", "West", "South", "East"])
        soil_type = st.selectbox("Soil Type", ["Sandy", "Loam", "Chalky", "Silt", "Clay", "Peaty"])
        crop = st.selectbox("Crop", ["Maize", "Rice", "Barley", "Wheat", "Cotton", "Soybean"])
        rainfall = st.number_input("Rainfall (mm)", min_value=0, max_value=5000)
        temperature = st.number_input("Temperature (Celsius)", min_value=-20, max_value=50)
        fertilizer_used = st.selectbox("Fertilizer Used", ["False", "True"])
        irrigation_used = st.selectbox("Irrigation Used", ["False", "True"])
        weather_condition = st.selectbox("Weather Condition", ["Sunny", "Rainy", "Cloudy"])
        days_to_harvest = st.number_input("Days to Harvest", min_value=1, max_value=365)
        
        submit_button = st.form_submit_button("Predict Yield")
    
    # Process the data and make prediction
    if submit_button:
        region_map = {"North": 1, "West": 3, "South": 2, "East": 0}
        soil_type_map = {"Sandy": 4, "Loam": 2, "Chalky": 0, "Silt": 5, "Clay": 1, "Peaty": 3}
        crop_map = {"Maize": 2, "Rice": 3, "Barley": 0, "Wheat": 5, "Cotton": 1, "Soybean": 4}
        weather_map = {"Sunny": 2, "Rainy": 1, "Cloudy": 0}
        
        data = [
            region_map[region],
            soil_type_map[soil_type],
            crop_map[crop],
            rainfall,
            temperature,
            1 if fertilizer_used == "True" else 0,
            1 if irrigation_used == "True" else 0,
            weather_map[weather_condition],
            days_to_harvest
        ]
        
        prediction = predict_crop_yield(data)
        
        st.success(f"Predicted Yield: {prediction:.2f} tons per hectare")

if __name__ == '__main__':
    main()
