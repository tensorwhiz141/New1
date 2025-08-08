import os
import requests
import docx
import PyPDF2
from flask import Flask, render_template, request, jsonify

# Your DeepInfra API Key (use environment variable for security)
API_KEY = os.environ.get("DEEPINFRA_API_KEY", "Zl4nc00K9QO28bOFXUtQOrk5GFgKYa1M")

# Model to use
MODEL_ID = "meta-llama/Meta-Llama-3.1-8B-Instruct"

POLICIES_FOLDER = "policies"

app = Flask(__name__)

def read_txt(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def read_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def read_pdf(file_path):
    text = ""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def load_policies():
    """Loads and concatenates text from all files in the policies folder."""
    context_parts = []
    if not os.path.exists(POLICIES_FOLDER):
        print(f"⚠️ Policies folder '{POLICIES_FOLDER}' not found.")
        return ""
    
    for filename in os.listdir(POLICIES_FOLDER):
        filepath = os.path.join(POLICIES_FOLDER, filename)
        if filename.lower().endswith(".txt"):
            context_parts.append(read_txt(filepath))
        elif filename.lower().endswith(".docx"):
            context_parts.append(read_docx(filepath))
        elif filename.lower().endswith(".pdf"):
            context_parts.append(read_pdf(filepath))
        else:
            print(f"Skipping unsupported file: {filename}")
    
    return "\n".join(context_parts)

def query_deepinfra(prompt, context=""):
    """Send a query to DeepInfra with optional context."""
    url = f"https://api.deepinfra.com/v1/inference/{MODEL_ID}"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    full_prompt = f"Context:\n{context}\n\nUser question: {prompt}\nAnswer based on the above context."
    
    payload = {"input": full_prompt}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [{}])[0].get("generated_text", "").strip()
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"

# Load policies once when the app starts
policy_context = load_policies()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data.get('question', '').strip()

    if not question:
        return jsonify({'error': 'Please provide a question'}), 400

    answer = query_deepinfra(question, policy_context)
    return jsonify({'answer': answer})

@app.route('/api/v1/hackrx/run', methods=['POST'])
def hackrx_webhook():
    """Webhook endpoint for HackRx testing platform"""
    try:
        # Get the request data
        data = request.get_json()

        # Extract question from the webhook payload
        # The testing platform might send different formats, so we'll handle multiple cases
        question = None
        if data:
            question = data.get('question') or data.get('query') or data.get('prompt') or data.get('input')

        # If no question in JSON, try form data
        if not question and request.form:
            question = request.form.get('question') or request.form.get('query') or request.form.get('prompt') or request.form.get('input')

        # If still no question, return error
        if not question:
            return jsonify({
                'status': 'error',
                'message': 'No question provided. Please include a question in the request.',
                'expected_format': {
                    'question': 'Your question about the policies'
                }
            }), 400

        # Process the question using our existing logic
        answer = query_deepinfra(question.strip(), policy_context)

        # Return response in a format expected by testing platforms
        return jsonify({
            'status': 'success',
            'question': question,
            'answer': answer,
            'timestamp': __import__('datetime').datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }), 500

@app.route('/api/v1/hackrx/health', methods=['GET'])
def health_check():
    """Health check endpoint for the webhook"""
    return jsonify({
        'status': 'healthy',
        'service': 'Policy Query System',
        'version': '1.0.0',
        'policies_loaded': len(policy_context) > 0
    })

if __name__ == "__main__":
    print("📄 Loading policies...")
    print("✅ Policies loaded! Starting web server...")
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
