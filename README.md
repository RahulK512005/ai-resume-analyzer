# AI Resume Analyzer

An AI-powered web application that analyzes resumes against job descriptions using Google's Gemini AI.

## Features

- **Resume Analysis**: Professional HR evaluation of candidate profiles
- **ATS Scoring**: Percentage match calculation with missing keywords
- **PDF Processing**: Converts resume PDFs to images for AI analysis
- **Real-time Results**: Instant feedback on resume-job alignment

## Live Demo

🚀 **[Try it now](https://ai-resume-analyzer-klit182wa-rahuls-projects-8971527f.vercel.app)**

## Tech Stack

- **Backend**: Flask (Python)
- **AI**: Google Gemini 2.5 Flash
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Vercel
- **PDF Processing**: pdf2image, Pillow

## Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/RahulK512005/ai-resume-analyzer.git
   cd ai-resume-analyzer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment**
   ```bash
   cp .env.example .env
   # Add your Google API key to .env
   ```

4. **Run locally**
   ```bash
   python api/index.py
   ```

### Deploy to Vercel

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Deploy**
   ```bash
   vercel --prod
   ```

3. **Set environment variables in Vercel dashboard**
   - `GOOGLE_API_KEY`: Your Google Gemini API key

## Usage

1. Enter job description
2. Upload PDF resume
3. Choose analysis type:
   - **Resume Review**: Professional evaluation
   - **Percentage Match**: ATS compatibility score
4. Get AI-powered insights

## API Setup

Get your Google API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open pull request

## License

MIT License