import os
import io
import PyPDF2
import streamlit as st
import google.generativeai as genai

# Page Configuration
st.set_page_config(
    page_title="AI Resume Analyzer & ATS Checker",
    page_icon="📄",
    layout="wide"
)

# Title & Subtitle
st.title("📄 AI Resume Analyzer & ATS Checker")
st.write("Evaluate your resume against job descriptions using Google Gemini AI!")

# Sidebar for API Key
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Enter Google Gemini API Key:", type="password")

if api_key:
    genai.configure(api_key=api_key)

# Function to extract text from uploaded PDF
def extract_pdf_text(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
    text = ""
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

# Input fields
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Upload Resume")
    uploaded_resume = st.file_uploader("Choose your Resume (PDF format)", type=["pdf"])

with col2:
    st.subheader("2. Job Description")
    job_description = st.text_area("Paste the Job Description here...", height=200)

# Action Buttons
st.divider()
col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    analyze_btn = st.button("📊 Detailed Resume Feedback", use_container_width=True)

with col_btn2:
    ats_btn = st.button("🎯 Calculate ATS Match Score", use_container_width=True)

# Processing Logic
if uploaded_resume and job_description:
    resume_text = extract_pdf_text(uploaded_resume)

    if analyze_btn:
        if not api_key:
            st.error("Please enter your Gemini API Key in the sidebar first!")
        else:
            with st.spinner("Analyzing resume against job description..."):
                prompt = f"""
                You are an expert HR Manager and Technical Recruiter. Analyze the following resume against the job description.
                
                Resume Text:
                {resume_text}

                Job Description:
                {job_description}

                Please provide a detailed review with the following sections:
                1. Executive Summary
                2. Key Strengths & Matching Skills
                3. Missing Skills & Keywords
                4. Actionable Suggestions for Improvement
                """
                
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt)
                
                st.subheader("📌 Resume Analysis Feedback")
                st.write(response.text)

    if ats_btn:
        if not api_key:
            st.error("Please enter your Gemini API Key in the sidebar first!")
        else:
            with st.spinner("Calculating ATS score..."):
                prompt = f"""
                You are an advanced Applicant Tracking System (ATS). Evaluate the resume against the provided job description.

                Resume Text:
                {resume_text}

                Job Description:
                {job_description}

                Provide the output in the following format:
                1. ATS Match Percentage (e.g., 75%)
                2. Missing Keywords (List important missing keywords)
                3. Final Verdict (Fit / Needs Improvement / Not Recommended)
                """
                
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt)
                
                st.subheader("🎯 ATS Compatibility Results")
                st.write(response.text)

elif (analyze_btn or ats_btn) and not (uploaded_resume and job_description):
    st.warning("Please upload a resume and paste a job description first!")
