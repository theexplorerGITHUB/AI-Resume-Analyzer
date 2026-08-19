import streamlit as st
import google.generativeai as genai
import PyPDF2 as pdf
import os

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

# Sidebar for API Key
st.sidebar.title("Configuration")
api_key_input = st.sidebar.text_input("Enter Google Gemini API Key:", type="password")

# Setup Gemini API
api_key = api_key_input or os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)

def get_gemini_response(prompt):
    model = genai.GenerativeModel('gemini-3.6-flash')
    response = model.generate_content(prompt)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page_text = reader.pages[page].extract_text()
        if page_text:
            text += page_text
    return text

st.title("📄 AI Resume Analyzer & ATS Checker")
st.caption("Evaluate your resume against job descriptions using Google Gemini AI!")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Upload Resume")
    uploaded_file = st.file_uploader("Choose your Resume (PDF format)", type=["pdf"])

with col2:
    st.subheader("2. Job Description")
    job_description = st.text_area("Paste the Job Description here...", height=200)

col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    btn_feedback = st.button("📊 Detailed Resume Feedback")

with col_btn2:
    btn_ats = st.button("🎯 Calculate ATS Match Score")

if btn_feedback or btn_ats:
    if not api_key:
        st.error("Please enter a valid Gemini API Key in the sidebar or Secrets!")
    elif uploaded_file is None or not job_description.strip():
        st.warning("Please upload a resume AND paste a job description first!")
    else:
        with st.spinner("Analyzing... Please wait..."):
            resume_text = input_pdf_text(uploaded_file)
            
            if btn_feedback:
                prompt = f"""
                You are an experienced HR/Recruiter. Analyze the given Resume against the Job Description.
                Provide feedback on Strengths, Weaknesses, and Suggestions for improvement.
                
                Resume: {resume_text}
                Job Description: {job_description}
                """
            else:
                prompt = f"""
                You are an advanced ATS (Applicant Tracking System) scanner. 
                Evaluate the match between the Resume and Job Description.
                Give an ATS Match Percentage (0-100%), Missing Keywords, and a Final Summary.
                
                Resume: {resume_text}
                Job Description: {job_description}
                """
            
            try:
                response = get_gemini_response(prompt)
                st.success("Analysis Complete!")
                st.markdown(response)
            except Exception as e:
                st.error(f"Error generating response: {e}")
