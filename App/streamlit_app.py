import streamlit as st
import pandas as pd
import joblib
from datetime import datetime

st.title("Sales Forecasting Dashboard")

# Load model
@st.cache_resource
def load_model():
    return joblib.load("model/sales_forecast_model.pkl")

model = load_model()

st.header("Enter Prediction Details")

store = st.number_input("Store ID", min_value=1)
item = st.number_input("Item ID", min_value=1)
date = st.date_input("Select Date")

if st.button("Predict Sales"):

    month = date.month
    week_of_year = date.isocalendar()[1]
    quarter = (month - 1) // 3 + 1
    day = date.day
    year = date.year
    day_of_week = date.weekday()

    is_weekend = 1 if day_of_week >= 5 else 0

    lag_1 = 0
    lag_7 = 0
    lag_30 = 0
    rolling_mean_7 = 0
    rolling_mean_30 = 0

    input_data = pd.DataFrame({
        "store":[store],
        "item":[item],
        "year":[year],
        "month":[month],
        "day":[day],
        "day_of_week":[day_of_week],
        "week_of_year":[week_of_year],
        "quarter":[quarter],
        "lag_1":[lag_1],
        "lag_7":[lag_7],
        "lag_30":[lag_30],
        "rolling_mean_7":[rolling_mean_7],
        "rolling_mean_30":[rolling_mean_30],
        "is_weekend":[is_weekend]
    })

    Feature_order = [
        "store",
        "item",
        "year",
        "month",
        "day",
        "day_of_week",
        "week_of_year",
        "quarter",
        "is_weekend",
        "lag_1",
        "lag_7",
        "lag_30",
        "rolling_mean_7",
        "rolling_mean_30",
        
    ]

    input_data = input_data[Feature_order]

    prediction = model.predict(input_data)

    st.success(f"Predicted Sales: {prediction[0]:.2f}")