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
st.title("📊 Data Analyst Bot with Python Execution")

# === SIDEBAR ===
st.sidebar.header("Upload & Settings")
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📋 Data Preview")
    st.dataframe(df.head())

    st.markdown("---")

    # === NATURAL LANGUAGE Q&A WITH CODE EXECUTION ===
    st.markdown("---")
    st.subheader("💬 Ask a Question About Your Data")

    user_question = st.text_input("Type your question and press Enter:")

    if user_question:
        # Prompt instructing the model to return pandas code only
        prompt = f"""
You are a professional data analyst using pandas in Python.

Given this DataFrame:

{df.head(5).to_string(index=False)}

Write Python pandas code to answer the question: "{user_question}"

Return only the code (a single line) that produces a DataFrame or Series result.

Do NOT include any explanations or text.
"""

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
            )
            code = response.choices[0].message.content.strip("```python\n").strip("```").strip()

            st.markdown("**Generated pandas code:**")
            st.code(code, language="python")

            # Execute the generated code safely in a restricted namespace
            # Provide the df so the code can use it
            local_vars = {"df": df, "pd": pd}
            exec(f"result = {code}", {}, local_vars)
            result = local_vars["result"]

            # Display the result (DataFrame or Series)
            if isinstance(result, pd.DataFrame) or isinstance(result, pd.Series):
                st.subheader("📊 Result:")
                st.dataframe(result)
            else:
                st.write(result)

            # Check if any matplotlib figure was created and display it
            import matplotlib.pyplot as plt
            if plt.get_fignums():
                st.pyplot(plt.gcf())
                plt.close('all')  # Close the figure so it doesn't overlap on next run

            # Optionally, ask the model to summarize the result
            summary_prompt = f"""
You wrote this pandas code:
{code}

The result of this code is:
{result.to_string() if isinstance(result, (pd.DataFrame, pd.Series)) else str(result)}

Please summarize this result in 1-2 sentences for a business user.
"""
            summary_response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": summary_prompt}],
                temperature=0.5,
            )
            summary = summary_response.choices[0].message.content.strip()
            st.markdown("**Summary:**")
            st.info(summary)

        except Exception as e:
            st.error(f"OpenAI or Execution error: {e}")

else:
    st.info("📁 Please upload a CSV file to get started.")