# AI Resume Analyzer

An AI-powered web application that analyzes resumes against job descriptions using OpenAI GPT-4o-mini.

## Features

- **Resume Analysis**: Professional HR evaluation of candidate profiles
- **ATS Scoring**: Percentage match calculation with missing keywords
- **PDF Processing**: Extracts text from PDF resumes for AI analysis
- **Real-time Results**: Instant feedback on resume-job alignment
- **Premium UI/UX**: Modern gradient design with drag-and-drop file upload

## Live Demo

🚀 **[Try it now](https://ai-resume-analyzer-jb16mqocg-rahuls-projects-8971527f.vercel.app)**

## Tech Stack

- **Backend**: Flask (Python)
- **AI**: OpenAI GPT-4o-mini
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Vercel
- **PDF Processing**: PyPDF2

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
   # Add your OpenAI API key to .env
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
   - `OPENAI_API_KEY`: Your OpenAI API key

## Usage

1. Enter job description
2. Upload PDF resume (drag-and-drop or click to browse)
3. Choose analysis type:
   - **Analyze Resume**: Professional HR evaluation
   - **ATS Score**: Compatibility percentage with missing keywords
4. Get AI-powered insights instantly

## API Setup

Get your OpenAI API key from [OpenAI Platform](https://platform.openai.com/api-keys)

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open pull request

## License

MIT License