import streamlit as st
import sympy as sp
import openai
import os

st.set_page_config(page_title="Sparx Maths Helper", page_icon="🔢")

st.title("🧠 Sparx Maths AI Helper")
st.write("Type your Sparx Maths question and get instant solutions!")

openai.api_key = st.secrets["OPENAI_API_KEY"]

def solve_with_sympy(expr_str):
    try:
        expr = sp.sympify(expr_str)
        simplified = sp.simplify(expr)
        return simplified
    except Exception as e:
        return f"Could not solve: {e}"

def explain_with_gpt(question, answer):
    prompt = (
        f"Explain step-by-step how to solve this maths problem:\n\n"
        f"Question: {question}\nAnswer: {answer}\n\n"
        f"Be clear and educational. Use bullet points if needed."
    )
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )
    return response["choices"][0]["message"]["content"]

# User input
question = st.text_input("📥 Enter your maths expression (e.g., '(2x + 3)(x - 5)'):")

if question:
    st.subheader("✅ Final Answer")
    result = solve_with_sympy(question)
    st.code(result, language="python")

    with st.spinner("🔍 Generating explanation..."):
        explanation = explain_with_gpt(question, result)
    st.subheader("📘 Step-by-Step Explanation")
    st.write(explanation)

