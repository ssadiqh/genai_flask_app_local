# Build Your First GenAI Application (Local Qwen Edition)

This is an **adapted version** of the IBM Skills Network course "Build Your First GenAI Application The Right Way" — but using **local Qwen2.5:7b via Ollama** instead of IBM Watsonx.

This tutorial teaches you how to build a production-quality GenAI Flask application step-by-step, with no API keys needed!

## 📚 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Project Structure](#project-structure)
3. [Tutorial: Step-by-Step](#tutorial-step-by-step)
4. [Running the Application](#running-the-application)
5. [Learning Outcomes](#learning-outcomes)
6. [Key Concepts](#key-concepts)
7. [Next Steps](#next-steps)

---

## Prerequisites

Before starting, ensure you have:

✅ **Ollama installed** with Qwen2.5:7b model
- Download from: https://ollama.ai
- Pull the model: `ollama pull qwen2.5:7b`
- Verify: `ollama serve` (should run on port 11434)

✅ **Python 3.9+** installed

✅ **Git** for version control

✅ **Basic knowledge of:**
- Python programming
- Flask web framework
- JSON data format
- REST APIs

---

## Project Structure

```
genai_flask_app_local/
├── config.py              # Configuration for local Qwen
├── model.py               # AI model integration with LangChain
├── app.py                 # Flask application (main backend)
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html         # Web interface
├── static/
│   ├── styles.css         # Styling
│   └── script.js          # Frontend logic
└── README.md              # This file
```

---

## Tutorial: Step-by-Step

### Step 1: Understanding LLMs (Large Language Models)

**Concept**: LLMs are AI models that predict the next token (word piece) based on context.

**Key Process**:
```
Text Input → Tokenization → Embeddings → Attention → Transformer Layers → Token Prediction → Text Output
```

**What you'll learn**:
- How tokenization breaks text into processable pieces
- How embeddings represent meaning in vector space
- How attention mechanisms understand context
- How transformer layers build sophisticated reasoning

### Step 2: Setting Up Your Environment

**What you'll do**:
1. Create a Python virtual environment
2. Install dependencies
3. Verify Ollama is running

**Commands**:
```bash
# Navigate to project directory
cd genai_flask_app_local

# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Or on Mac/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**What gets installed**:
- `Flask`: Web framework for building the API
- `langchain-ollama`: Integration with local Qwen
- `langchain-core`: Core LangChain abstractions
- `pydantic`: Data validation and structured outputs

### Step 3: Configuration (`config.py`)

**What you'll learn**:
- How to centralize model settings
- Key parameters for LLM behavior:
  - `temperature`: Controls randomness (0.3 = consistent, 0.9 = creative)
  - `max_tokens`: Limits response length
  - `base_url`: Points to local Ollama server

**Key file location**: [config.py](config.py)

**Important settings**:
```python
PARAMETERS = {
    "temperature": 0.3,      # Lower = more consistent
    "max_tokens": 256,       # Response length limit
}

CREDENTIALS = {
    "model": "qwen2.5:7b",
    "base_url": "http://localhost:11434"  # Local Ollama
}
```

### Step 4: Model Integration (`model.py`)

**What you'll learn**:
- How to define structured outputs with Pydantic
- How to use LangChain's JsonOutputParser
- How to chain prompts with models
- How to use special tokens for Qwen

**Key components**:

#### A. Define Response Structure
```python
class AIResponse(BaseModel):
    summary: str              # Summarize user message
    sentiment: int (0-100)   # Emotional tone
    response: str            # AI's reply
```

#### B. Initialize Model
```python
qwen_llm = OllamaLLM(
    model="qwen2.5:7b",
    base_url="http://localhost:11434"
)
```

#### C. Create Prompt Template
```python
qwen_template = PromptTemplate(
    template="""<|im_start|>system
{system_prompt}
{format_prompt}<|im_end|>
<|im_start|>user
{user_prompt}<|im_end|>
<|im_start|>assistant
""",
    input_variables=["system_prompt", "format_prompt", "user_prompt"]
)
```

#### D. Chain Everything Together
```python
def get_ai_response(model, template, system_prompt, user_prompt):
    # Flow: Template -> Model -> JSON Parser
    chain = template | model | json_parser
    return chain.invoke({...})
```

**Key file location**: [model.py](model.py)

### Step 5: Flask Application (`app.py`)

**What you'll learn**:
- How to create REST API endpoints
- How to handle JSON requests/responses
- How to measure AI response time
- How to add error handling and logging

**Key endpoints**:

#### GET / (Home)
Returns the web interface (index.html)

#### POST /generate (Main AI Endpoint)
```json
Request: {"message": "What is Python?", "model": "qwen"}
Response: {
    "summary": "User asking about Python",
    "sentiment": 50,
    "response": "Python is a versatile programming language...",
    "duration": 2.45
}
```

#### GET /health (Health Check)
Returns API status

**Key file location**: [app.py](app.py)

### Step 6: Web Interface (`templates/index.html`)

**What you'll learn**:
- How to build a chat interface
- How to handle user input with HTML forms
- How to structure the UI for messaging apps

**Key features**:
- Model selection dropdown
- Message input with auto-expanding textarea
- Chat message display
- Loading indicators
- Clear chat button

**Key file location**: [templates/index.html](templates/index.html)

### Step 7: Frontend Logic (`static/script.js`)

**What you'll learn**:
- How to make asynchronous API calls
- How to manage chat state
- How to update the UI dynamically
- How to handle user interactions

**Key functions**:
- `handleSendMessage()`: Send user message to API
- `addMessage()`: Display message in chat
- `showLoading()`: Show thinking indicator
- `clearChat()`: Reset conversation

**Key file location**: [static/script.js](static/script.js)

### Step 8: Styling (`static/styles.css`)

**What you'll learn**:
- How to create a modern chat UI
- How to use gradients and animations
- How to make responsive design

**Visual features**:
- Purple gradient header
- Clean message bubbles
- Loading animations
- Mobile-responsive layout

**Key file location**: [static/styles.css](static/styles.css)

---

## Running the Application

### 1. Start Ollama Server
```bash
ollama serve
```
Keep this running in a separate terminal.

### 2. Install Dependencies (First time only)
```bash
pip install -r requirements.txt
```

### 3. Run Flask Application
```bash
python app.py
```

You'll see:
```
 * Running on http://localhost:5000
 * Debug mode: on
```

### 4. Access the Application
Open your browser and go to: **http://localhost:5000**

### 5. Test the Application
1. Type a message (e.g., "What is machine learning?")
2. Click Send or press Enter
3. Watch as Qwen processes and responds
4. See the response time at the bottom

---

## Learning Outcomes

By completing this tutorial, you'll understand:

✅ **How LLMs work**
- Tokenization and embeddings
- Attention mechanisms
- Transformer architecture

✅ **How to integrate LLMs into applications**
- Using LangChain for abstraction
- Connecting to local models
- Parsing structured outputs

✅ **How to build production-ready AI apps**
- Proper error handling
- Logging and monitoring
- Modular code architecture

✅ **How to create intuitive AI interfaces**
- Real-time chat UI
- Loading states
- Response formatting

✅ **Prompt engineering fundamentals**
- System vs. user prompts
- Special tokens (for different models)
- JSON output formatting

---

## Key Concepts

### 1. Special Tokens (Qwen Format)
```
<|im_start|>system    <- Role: System instructions
<|im_end|>            <- End of previous message
<|im_start|>user      <- Role: User message
<|im_start|>assistant <- Role: AI response
```

### 2. Temperature
- **0.0 - 0.3**: Precise, consistent, factual
- **0.5 - 0.7**: Balanced, creative
- **0.8 - 1.0**: Creative, varied, less predictable

### 3. JSON Output Parsing
```python
# Define structure
class Response(BaseModel):
    field1: str
    field2: int

# Parse outputs
parser = JsonOutputParser(pydantic_object=Response)
chain = prompt | model | parser  # Automatic JSON parsing
```

### 4. LangChain Chains
```python
# The pipe operator (|) chains components
chain = prompt_template | llm | output_parser

# Equivalent to:
# 1. Format prompt with variables
# 2. Send to LLM
# 3. Parse the output
```

---

## Next Steps

### Basic Enhancements
1. **Add conversation memory**: Keep message history for context
2. **Add sentiment visualization**: Show sentiment scores graphically
3. **Add response time tracking**: Chart performance over time

### Intermediate Enhancements
4. **Compare multiple models**: Add more Qwen variants or other models
5. **Add caching**: Cache responses for common questions
6. **Implement search**: Add RAG (Retrieval-Augmented Generation)

### Advanced Enhancements
7. **Multi-turn conversations**: Maintain context across messages
8. **A/B testing**: Compare different prompt strategies
9. **Analytics dashboard**: Track usage and performance

### Production Features
10. **Database integration**: Store chat history
11. **User authentication**: Add login system
12. **Rate limiting**: Prevent abuse
13. **Monitoring**: Add Prometheus/Grafana metrics

---

## Troubleshooting

### Problem: "Connection refused on port 11434"
**Solution**: Make sure Ollama is running
```bash
ollama serve
```

### Problem: "Model not found: qwen2.5:7b"
**Solution**: Pull the model first
```bash
ollama pull qwen2.5:7b
```

### Problem: Flask won't start on port 5000
**Solution**: Port might be in use. Change in app.py:
```python
app.run(debug=True, port=5001)  # Use different port
```

### Problem: Slow responses
**Solution**: This is normal for local Qwen
- Responses take 2-5 seconds
- Ensure no other heavy processes are running
- Try restarting Ollama

---

## Key Files Reference

| File | Purpose | Key Learning |
|------|---------|--------------|
| `config.py` | Centralized settings | Configuration management |
| `model.py` | AI integration | LangChain & Pydantic |
| `app.py` | Backend API | Flask & REST APIs |
| `index.html` | Web interface | HTML structure |
| `script.js` | Frontend logic | Async API calls |
| `styles.css` | Visual design | Modern CSS |

---

## Learning Resources

### Within This Project
- Read code comments: Each file has inline explanations
- Experiment: Try changing parameters in `config.py`
- Debug: Use browser DevTools to see API requests

### External Resources
- [LangChain Docs](https://python.langchain.com/)
- [Ollama Documentation](https://github.com/ollama/ollama)
- [Flask Tutorial](https://flask.palletsprojects.com/)
- [Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)

---

## Summary

You've built a complete GenAI application with:
- ✅ Local LLM integration (no API keys)
- ✅ Structured JSON outputs
- ✅ Modern web interface
- ✅ Production-quality error handling
- ✅ Step-by-step learning path

**Next**: Read through each file in order (config.py → model.py → app.py → templates/index.html → static/script.js) to understand how it all works together!

---

**Last Updated**: June 2026
**Model**: Qwen 2.5:7b (Local)
**Framework**: LangChain + Flask