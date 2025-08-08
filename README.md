# HackRx 6.0 - LLM Document Query System

A web-based AI-powered document query system that allows users to ask questions about policy documents and get intelligent answers using DeepInfra's LLM API.

## 🚀 Quick Start

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the web application
python main.py

# Visit http://127.0.0.1:5000 in your browser
```

## 🌐 Web Deployment

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed deployment instructions to Heroku, Railway, or Render.

## 📁 Project Structure

- `main.py` - Flask web application
- `policies/` - Directory containing policy documents (PDF, DOCX, TXT)
- `templates/index.html` - Web interface
- `requirements.txt` - Python dependencies
- `Procfile` - Deployment configuration
