import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv
from openai import OpenAI

# === Load API Key ===
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# === Streamlit UI Setup ===
st.set_page_config(page_title="CSV Analyst Bot", layout="wide")
st.title("📊 CSV Data Analyst Bot")

# === SIDEBAR ===
st.sidebar.header("Upload & Settings")
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type="csv")
chart_type = st.sidebar.selectbox("Select chart type", ["None", "Line Chart", "Bar Chart", "Heatmap"])

# === MAIN FUNCTIONALITY ===
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📋 Data Preview")
    st.dataframe(df.head())

    st.markdown("---")

        # === CHART RENDERING ===
    if chart_type != "None":
        st.subheader(f"📊 {chart_type}")
        
        numeric_columns = df.select_dtypes(include='number').columns.tolist()
        all_columns = df.columns.tolist()

        if chart_type in ["Line Chart", "Bar Chart"]:
            x_axis = st.selectbox("Select X-axis", options=all_columns)
            y_axis = st.selectbox("Select Y-axis", options=numeric_columns)

            if x_axis and y_axis:
                chart_data = df[[x_axis, y_axis]].dropna()
                chart_data = chart_data.sort_values(by=x_axis)
                
                if chart_type == "Line Chart":
                    st.line_chart(chart_data.set_index(x_axis))
                elif chart_type == "Bar Chart":
                    st.bar_chart(chart_data.set_index(x_axis))

        elif chart_type == "Heatmap":
            if numeric_columns:
                corr = df[numeric_columns].corr()
                fig, ax = plt.subplots()
                sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
                st.pyplot(fig)
            else:
                st.warning("No numeric columns found for heatmap.")


    # === QUESTION ANSWERING ===
    st.markdown("---")
    st.subheader("💬 Ask a Question About Your Data")
    user_question = st.text_input("Type your question and press Enter:")

    if user_question:
        prompt = f"""
You are a professional data analyst. You are analyzing the following dataset:

{df.head(5).to_string(index=False)}

User question: {user_question}
Please provide your answer using only the information shown above.
"""

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
            )
            answer = response.choices[0].message.content
            st.markdown("**Insight:**")
            st.success(answer)
        except Exception as e:
            st.error(f"OpenAI error: {e}")

else:
    st.info("📁 Please upload a CSV file to get started.")
