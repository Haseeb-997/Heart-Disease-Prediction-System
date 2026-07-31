import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title = "Heart Disease Predictor", page_icon = "🫀", layout = "wide")

model = joblib.load("Logistic_Regression_heart_model.pkl")
scaler = joblib.load("heart_scaler.pkl")
expected_columns = joblib.load("heart_columns.pkl")

st.title("🫀 Heart Disease Risk Prediction")
st.caption("Developed by Muhammad Haseeb")

c1, c2 = st.columns(2)
with c1:
    age = st.slider("Age", 18, 100, 40)
    sex = st.selectbox("Sex", ["M", "F"])
    chest = st.selectbox("Chest Pain", ["ATA", "NAP", "TA", "ASY"])
    bp = st.number_input("Resting BP", 80, 220, 120)
    chol = st.number_input("Cholesterol", 100, 600, 200)
with c2:
    fbs = st.selectbox("Fasting BS > 120", [0, 1])
    ecg = st.selectbox("Resting ECG", ["Normal", "ST", "LVH"])
    hr = st.slider("Max HR", 60, 220, 150)
    ang = st.selectbox("Exercise Angina", ["Y", "N"])
    old = st.slider("Oldpeak", 0.0, 6.0, 1.0)
    slope = st.selectbox("ST Slope", ["Up", "Flat", "Down"])

if st.button("🚀 Predict", use_container_width = True):
    raw={
        "Age" : age,
        "RestingBP" : bp,
        "Cholesterol" : chol,
        "FastingBS" : fbs,
        "MaxHR" : hr,
        "Oldpeak" : old,
        "Sex_" + sex : 1,
        "ChestPainType_" + chest : 1,
        "RestingECG_" + ecg : 1,
        "ExerciseAngina_" + ang : 1,
        "ST_Slope_" + slope : 1
    }

    df = pd.DataFrame([raw])

    for col in expected_columns:
        if col not in df.columns:
            df[col] = 0

    df = df[expected_columns]

    X = scaler.transform(df)

    pred = model.predict(X)[0]

    prob = model.predict_proba(X)[0][1]

    st.metric("Risk Probability", f"{prob*100:.1f}%")
    st.progress(float(prob))

    if pred == 1:
        st.error("⚠️ High Risk of Heart Disease")
    else:
        st.success("✅ Low Risk of Heart Disease")

    st.subheader("Input Summary")
    st.dataframe(df,use_container_width = True)