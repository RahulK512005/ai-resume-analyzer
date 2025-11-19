from flask import Flask, request, render_template, jsonify
from dotenv import load_dotenv
import base64
import os
import io
import PyPDF2
from openai import OpenAI
import httpx

load_dotenv()

app = Flask(__name__, template_folder='../templates')
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    timeout=httpx.Timeout(60.0, connect=10.0),
    max_retries=2
)

def get_openai_response(input_text, pdf_text, prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"Job Description:\n{input_text}\n\nResume:\n{pdf_text[:4000]}"}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"OpenAI API error: {str(e)}")

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
        
        if not pdf_content or len(pdf_content.strip()) < 50:
            return jsonify({'error': 'Could not extract text from PDF. Please ensure the PDF contains readable text.'}), 400
        
        response = get_openai_response(job_description, pdf_content, prompt)
        return jsonify({'response': response})
        
    except Exception as e:
        error_msg = str(e)
        if 'API key' in error_msg:
            return jsonify({'error': 'API key configuration error. Please contact support.'}), 500
        elif 'timeout' in error_msg.lower():
            return jsonify({'error': 'Request timeout. Please try again.'}), 500
        else:
            return jsonify({'error': f'Error: {error_msg}'}), 500

if __name__ == '__main__':
    app.run(debug=True)