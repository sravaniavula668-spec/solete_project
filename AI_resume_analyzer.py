import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import os

# -------------------------------
# Load Environment Variables
# -------------------------------
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

# -------------------------------
# Streamlit Page
# -------------------------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Resume Analyzer")
st.write("Upload your resume and receive AI-powered feedback.")

uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

# -------------------------------
# Extract PDF Text
# -------------------------------
def extract_text(pdf_file):
    reader = PdfReader(pdf_file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text

# -------------------------------
# Analyze Resume
# -------------------------------
if uploaded_file is not None:

    resume_text = extract_text(uploaded_file)

    st.subheader("Extracted Resume Text")

    st.text_area(
        "",
        resume_text,
        height=250
    )

    if st.button("Analyze Resume"):

        prompt = f"""
You are an expert HR Recruiter and ATS Resume Reviewer.

Analyze the following resume.

Return the response using these headings.

# Resume Summary

# Strengths

# Weaknesses

# Improvement Suggestions

# ATS Score (Out of 100)

Explain why you gave this score.

# Missing Skills

Suggest important skills that should be added.

# Final Recommendation

Should this resume be shortlisted?

Resume:

{resume_text}
"""

        with st.spinner("Analyzing Resume..."):

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3
            )

        result = response.choices[0].message.content

        st.success("Analysis Complete!")

        st.markdown(result)