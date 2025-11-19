from flask import Flask, request, render_template, jsonify
from dotenv import load_dotenv
import base64
import os
import io
import PyPDF2
from openai import OpenAI

load_dotenv()

app = Flask(__name__, template_folder='../templates')
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_openai_response(input_text, pdf_text, prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Job Description:\n{input_text}\n\nResume:\n{pdf_text}"}
        ]
    )
    return response.choices[0].message.content

def input_pdf_setup(uploaded_file):
    if uploaded_file:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    else:
        raise FileNotFoundError("No file uploaded")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    try:
        job_description = request.form.get('job_description', '').strip()
        analysis_type = request.form.get('analysis_type')
        uploaded_file = request.files.get('resume')
        
        if not uploaded_file or uploaded_file.filename == '':
            return jsonify({'error': 'Please upload a resume PDF file'}), 400
        
        if not uploaded_file.filename.lower().endswith('.pdf'):
            return jsonify({'error': 'Only PDF files are supported'}), 400
            
        pdf_content = input_pdf_setup(uploaded_file)
        
        if analysis_type == 'review':
            prompt = """You are an experienced Technical Human Resource Manager. Review the provided resume against the job description. 
            Share your professional evaluation on whether the candidate's profile aligns with the role. 
            Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements."""
        else:
            prompt = """You are a skilled ATS (Applicant Tracking System) scanner with deep understanding of ATS functionality. 
            Evaluate the resume against the provided job description. Give the percentage of match if the resume matches the job description. 
            Format: First show percentage, then keywords missing, and finally your thoughts."""
        
        response = get_openai_response(job_description, pdf_content, prompt)
        return jsonify({'response': response})
        
    except Exception as e:
        return jsonify({'error': f'Error processing resume: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)