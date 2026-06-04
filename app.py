# Flask Application with Local Qwen AI Integration
# This is the main backend for the GenAI application

from flask import Flask, request, jsonify, render_template
from model import qwen_response
import time
import logging

# ============================================
# Setup Logging
# ============================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================
# Initialize Flask App
# ============================================
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# ============================================
# Routes
# ============================================

@app.route('/', methods=['GET'])
def index():
    """Serve the main HTML page"""
    logger.info("User accessed home page")
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    """
    Main AI endpoint that processes user messages

    Expected JSON input:
    {
        "message": "User's question",
        "model": "qwen"
    }

    Returns:
    {
        "summary": "Summary of user message",
        "sentiment": 75,
        "response": "AI's response",
        "duration": 2.45
    }
    """
    try:
        # Get JSON data from request
        data = request.json
        user_message = data.get('message')
        model = data.get('model', 'qwen')  # Default to qwen

        # Validate input
        if not user_message or not user_message.strip():
            logger.warning("Empty message received")
            return jsonify({"error": "Message cannot be empty"}), 400

        if model != 'qwen':
            logger.warning(f"Invalid model requested: {model}")
            return jsonify({"error": "Only 'qwen' model is available"}), 400

        logger.info(f"Processing message from {model} model: {user_message[:50]}...")

        # Define system prompt
        system_prompt = """You are an AI assistant helping with customer inquiries.
Provide a helpful and concise response.
Analyze the sentiment of the user's message (0=very negative, 100=very positive).
Provide a summary of what the user asked."""

        # Measure response time
        start_time = time.time()

        # Get AI response
        if model == 'qwen':
            result = qwen_response(system_prompt, user_message)

        # Add duration to response
        duration = time.time() - start_time
        result['duration'] = round(duration, 2)

        logger.info(f"Generated response in {duration:.2f} seconds")
        return jsonify(result)

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({"error": f"Error processing request: {str(e)}"}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "model": "qwen2.5:7b"})

# ============================================
# Error Handlers
# ============================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({"error": "Internal server error"}), 500

# ============================================
# Run Application
# ============================================

if __name__ == '__main__':
    logger.info("Starting Flask application with Local Qwen2.5:7b")
    logger.info("Make sure Ollama is running with: ollama serve")
    logger.info("Access the app at http://localhost:5000")
    app.run(debug=True, host='localhost', port=5000)