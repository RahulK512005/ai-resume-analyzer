from flask import Flask, request, render_template, jsonify
from dotenv import load_dotenv
import base64
import os
import io
from PIL import Image
import pdf2image
import google.generativeai as genai

load_dotenv()

app = Flask(__name__, template_folder='../templates')
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash') 
    response = model.generate_content([prompt, pdf_content[0], input_text])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]
        
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [{
            "mime_type": "image/jpeg",
            "data": base64.b64encode(img_byte_arr).decode()
        }]
        return pdf_parts
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
        
        response = get_gemini_response(job_description, pdf_content, prompt)
        return jsonify({'response': response})
        
    except Exception as e:
        return jsonify({'error': f'Error processing resume: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)