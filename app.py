import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load your trained model
model = joblib.load("cyber_model.pkl")

st.title("🧠 AI-Powered Cyber Threat Detection System")
st.write("This app uses your trained Machine Learning model to detect potential cyber threats based on network parameters.")

# Sidebar mode selector
mode = st.sidebar.radio("Choose Mode", ["Single Input", "Batch Upload (CSV)"])

if mode == "Single Input":
    st.subheader("🔹 Single Data Prediction")
    packet_size = st.slider("Packet Size (bytes)", 20, 1500, 300)
    duration = st.slider("Connection Duration (seconds)", 0.0, 10.0, 1.0)
    src_bytes = st.number_input("Source Bytes", 0, 10000, 1000)
    dst_bytes = st.number_input("Destination Bytes", 0, 10000, 800)

    input_data = np.array([[packet_size, duration, src_bytes, dst_bytes]])
    prediction = model.predict(input_data)[0]
    st.success(f"🚨 Predicted Threat Type: **{prediction.upper()}**")

else:
    st.subheader("📁 Batch Detection via CSV Upload")
    uploaded_file = st.file_uploader("Upload a CSV file with columns: packet_size, duration, src_bytes, dst_bytes", type=["csv"])

    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.write("### Uploaded Data Preview:")
        st.dataframe(data.head())

        try:
            preds = model.predict(data)
            data["Predicted_Threat"] = preds
            st.success("✅ Predictions generated successfully!")
            st.write("### Results:")
            st.dataframe(data)

            csv = data.to_csv(index=False).encode('utf-8')
            st.download_button("⬇️ Download Predictions as CSV", data=csv, file_name="predicted_threats.csv", mime="text/csv")
        except Exception as e:
            st.error(f"❌ Error: {e}")
