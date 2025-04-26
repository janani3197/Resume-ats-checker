from dotenv import load_dotenv

load_dotenv()
import streamlit as st
import fitz  # <--- pymupdf
import google.generativeai as genai
import os
import io
import base64
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Open the uploaded PDF using pymupdf
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        first_page = doc.load_page(0)  # Load first page

        pix = first_page.get_pixmap(dpi=200)  # Higher DPI for better quality
        img_bytes_arr = io.BytesIO(pix.tobytes("jpeg"))  # Save as JPEG in memory

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_bytes_arr.getvalue()).decode(),
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded. Please upload a PDF file.")
    
# Streamlit app
st.set_page_config(page_title="RESUME ATS CHECKER", page_icon=":guardsman:", layout="wide")
st.header("RESUME ATS CHECKER")
input_text = st.text_area("Paste the job description here:", key="input")
uploaded_file = st.file_uploader("Upload your resume here:", type=["pdf"])

if uploaded_file is not None:
    st.write("File uploaded successfully!")

submit1 = st.button("Tell me about Resume")
submit2 = st.button("Rewrite resume")
submit3 = st.button("Percentage match")
submit4 = st.button("How can I improve my resume for this job description")

input_prompt1 = """
You are an experienced HR with technical expert experience in the field of any one job role from data science, full stack web development, 
big data engineering, DevOps, data analyst. Your task is to review the provided resume against the job description 
for these profiles. 
Please share your professional evaluation on whether the candidate's profile aligns with the job description. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job description.
"""

input_prompt2 = """
You are an experienced resume writer with technical expertise in the field of any one job role from data science, full stack web development,
big data engineering, DevOps, data analyst. Your task is to rewrite the technical skills section of the resume and the work experience section
to make it more ATS friendly and align it with the experience and skills mentioned in the job description. When giving work experience bullet points,
always quantify with metrics and numbers.
"""

input_prompt3 = """
You are a very skilled ATS (Application Tracking System) scanner with a deep understanding of any one job role: data science, 
full stack web development, big data engineering, DevOps, data analyst, and deep ATS functionality. 
Your task is to evaluate the resume against the provided job description, giving me the percentage match of resume 
with the job description. First, the output should come as a percentage, and then list the keywords missing in the resume from the job description as bullet points.
"""

input_prompt4 = """
You are an experienced resume writer with technical expertise in the field of any one job role from data science, full stack web development,
big data engineering, DevOps, data analyst. Your task as a very experienced resume writer is to provide me with suggestions on how my resume could be improved for the job description.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("Response:")
        st.write(response)
    else:
        st.write("Please upload a PDF file to get a response.")

elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2, pdf_content, input_text)
        st.subheader("Response:")
        st.write(response)
    else:
        st.write("Please upload a PDF file to get a response.")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("Response:")
        st.write(response)
    else:
        st.write("Please upload a PDF file to get a response.")

elif submit4:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt4, pdf_content, input_text)
        st.subheader("Response:")
        st.write(response)
    else:
        st.write("Please upload a PDF file to get a response.")
