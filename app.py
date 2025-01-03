import os
import streamlit as st
from groq import Groq
from fpdf import FPDF  # For PDF generation

api = "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"

# --- Groq API Setup ---
client = Groq(api_key=api)

# Function to get code from StarCoder model
def generate_code(summary, language):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Generate efficient {language} code for the following task without any explanations or comments: {summary}",
                }
            ],
            model="llama3-8b-8192",  # Specify the model
            stream=False,
        )
        generated_code = chat_completion.choices[0].message.content
        return generated_code
    except Exception as e:
        st.error(f"Error generating code: {e}")
        return ""

# Function to explain the generated code using Llama
def explain_code(code):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Explain the following code descriptively and attractively so the user can easily understand it:\n\n{code}",
                }
            ],
            model="llama3-8b-8192",
            stream=False,
        )
        explanation = chat_completion.choices[0].message.content
        return explanation
    except Exception as e:
        st.error(f"Error explaining code: {e}")
        return ""

# Function to save code as a PDF
def save_code_as_pdf(code, file_name="generated_code.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, code)
    pdf.output(file_name)
    return file_name

# --- Streamlit Interface ---
st.set_page_config(page_title="Generative AI Code Generator", page_icon="🧑‍💻", layout="wide")

# Page Title
st.title("🚀 Generative AI Code Generator Using StarCoder")

# Input Fields
summary = st.text_area("📝 Enter the Task Summary", "For example: Create a function to add two numbers.")
language = st.selectbox("🌐 Select Programming Language", ["Python", "Java", "JavaScript", "C++"])

# Generate Code Button
if st.button("Generate Code"):
    if summary:
        generated_code = generate_code(summary, language)

        if generated_code:
            st.subheader(f"✨ Generated {language} Code:")
            st.code(generated_code, language=language.lower())

            # Code Modification Section
            modified_code = st.text_area("✏️ Modify the Code (Optional):", value=generated_code, height=200)

            # Explanation Button
            if st.button("Explain Code"):
                explanation = explain_code(generated_code)
                st.subheader("📖 Code Explanation:")
                st.write(explanation)

            # Download Code as PDF
            if st.button("Download Code as PDF"):
                pdf_path = save_code_as_pdf(modified_code)  # Use modified code if edited
                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(
                        label="📥 Download PDF",
                        data=pdf_file,
                        file_name="generated_code.pdf",
                        mime="application/pdf",
                    )

# New Code Button
if st.button("Generate New Code"):
    st.rerun()  # Refresh the page to clear inputs

# Footer Information
st.markdown("---")
st.write("🌟 Powered by **Streamlit**, **Groq**, and **StarCoder** | Deployed on Hugging Face")
