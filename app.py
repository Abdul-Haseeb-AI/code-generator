
import os
import streamlit as st
from groq import Groq

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
            model="llama3-8b-8192",  # Specify the model you want to use
            stream=False,
        )
        generated_code = chat_completion.choices[0].message.content
        return generated_code
    except Exception as e:
        st.error(f"Error generating code: {e}")
        return ""

# --- Streamlit Interface ---
st.set_page_config(page_title="Generative AI Code Generator", page_icon="👨‍💻", layout="wide")

# Page Title
st.title("Generative AI Code Generator Using StarCoder")

# Summary Input
summary = st.text_area("Enter the Summary of the Task", "For example: Create a function to add two numbers.")
language = st.selectbox("Select the Programming Language", ["Python", "Java", "JavaScript", "C++"])

# Generate Code Button
if st.button("Generate Code"):
    if summary:
        # Generate the code using Groq and StarCoder
        generated_code = generate_code(summary, language)

        if generated_code:
            st.subheader(f"Generated {language} Code:")
            st.code(generated_code, language=language.lower())

            # Modify or remove sections of code (optional)
            modified_code = st.text_area("Modify the Code (Optional)", value=generated_code, height=200)

            # Download Code Button (Download as TXT)
            st.download_button(
                label="Download Code",
                data=modified_code or generated_code,  # Use modified_code if edited, otherwise generated_code
                file_name="generated_code.txt",
                mime="text/plain"
            )

# New Code Button
if st.button("Generate New Code"):
    summary = ""  # Clear the summary input
    st.rerun()  # Refresh the page to clear inputs

# Footer Information
st.markdown("---")
st.write("💻 Powered by Streamlit | AI Code Generation by Groq and StarCoder")
