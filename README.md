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
- `langchain-ollama`: Integration with local Qwen (includes langchain-core)
- `pydantic`: Data validation and structured outputs
- `requests`: HTTP client for API calls

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

## Complete Request Flow: How It All Works Together

This diagram shows what happens when you send a message:

```
┌─────────────────────────────────────────────────────────────────────┐
│ 1. BROWSER (JavaScript - static/script.js)                          │
│    User types: "What is machine learning?"                          │
│    Clicks Send                                                       │
└────────────────────────┬────────────────────────────────────────────┘
                         │ POST /generate
                         │ {"message": "What is machine learning?", "model": "qwen"}
                         ↓
┌─────────────────────────────────────────────────────────────────────┐
│ 2. FLASK SERVER (app.py - routes/generate endpoint)                 │
│    Receives JSON request                                            │
│    Validates: ✅ message not empty, ✅ model is qwen                │
│    Extracts: user_message, model type                               │
│    Logs: "Processing message from qwen model..."                    │
│    Measures time: start_time = now                                  │
└────────────────────────┬────────────────────────────────────────────┘
                         │ Calls: qwen_response(system_prompt, user_message)
                         ↓
┌─────────────────────────────────────────────────────────────────────┐
│ 3. LANGCHAIN PIPELINE (model.py)                                    │
│                                                                      │
│    ┌─────────────────────────────────────────────────────────────┐  │
│    │ STEP 1: PromptTemplate (qwen_template)                      │  │
│    │ ─────────────────────────────────────                       │  │
│    │ Formats prompt with special Qwen tokens:                    │  │
│    │                                                              │  │
│    │ <|im_start|>system                                           │  │
│    │ You are an AI assistant...                                   │  │
│    │ Analyze sentiment (0-100)...                                 │  │
│    │ [format instructions from JsonOutputParser]                  │  │
│    │ <|im_end|>                                                   │  │
│    │ <|im_start|>user                                             │  │
│    │ What is machine learning?<|im_end|>                          │  │
│    │ <|im_start|>assistant                                        │  │
│    └──────────────────────┬──────────────────────────────────────┘  │
│                           ↓                                          │
│    ┌─────────────────────────────────────────────────────────────┐  │
│    │ STEP 2: OllamaLLM (qwen_llm)                                │  │
│    │ ─────────────────────────────                               │  │
│    │ Sends HTTP POST to http://localhost:11434                   │  │
│    │ Model: "qwen2.5:7b"                                         │  │
│    │ Temperature: 0.3 (from config.py)                           │  │
│    │ Max tokens: 256 (from config.py)                            │  │
│    └──────────────────────┬──────────────────────────────────────┘  │
│                           ↓                                          │
└───────────────────────────┼──────────────────────────────────────────┘
                            │
┌───────────────────────────┼──────────────────────────────────────────┐
│ 4. OLLAMA SERVER (localhost:11434)                                   │
│                                                                       │
│    ┌──────────────────────────────────────────────────────────────┐  │
│    │ Loads qwen2.5:7b model (7 billion parameters)               │  │
│    │ Tokenizes: "What is machine learning?" → [What][is]...      │  │
│    │ Creates embeddings: token → [0.2, -0.5, 0.8, ...]          │  │
│    │                                                              │  │
│    │ TRANSFORMER LAYERS (32 iterations):                         │  │
│    │ Layer 1: Basic relationships                                │  │
│    │ Layer 2: Phrase understanding                               │  │
│    │ ...                                                         │  │
│    │ Layer 32: Deep contextual reasoning                         │  │
│    │                                                              │  │
│    │ TOKEN GENERATION (iterative):                               │  │
│    │ Predicts: "Machine" (confidence: 0.95)                      │  │
│    │ Predicts: "learning" (confidence: 0.98)                     │  │
│    │ Predicts: "is" (confidence: 0.92)                           │  │
│    │ ... continues for up to 256 tokens                          │  │
│    │                                                              │  │
│    │ Final output:                                               │  │
│    │ {"summary": "User asking about ML", "sentiment": 50,        │  │
│    │  "response": "Machine learning is a subset of AI..."}       │  │
│    │                                                              │  │
│    │ ⏱️  Takes ~10-15 seconds total                              │  │
│    └──────────────────────┬───────────────────────────────────────┘  │
│                           ↓                                          │
└───────────────────────────┼──────────────────────────────────────────┘
                            │ Returns raw JSON text
                            ↓
┌───────────────────────────┼──────────────────────────────────────────┐
│ 5. LANGCHAIN PIPELINE (continued)                                    │
│                                                                       │
│    ┌──────────────────────────────────────────────────────────────┐  │
│    │ STEP 3: JsonOutputParser                                     │  │
│    │ ──────────────────────────────                               │  │
│    │ Receives raw text with embedded JSON                         │  │
│    │ Extracts JSON object                                         │  │
│    │ Validates against AIResponse schema:                         │  │
│    │   - summary: must be string ✅                               │  │
│    │   - sentiment: must be int 0-100 ✅                          │  │
│    │   - response: must be string ✅                              │  │
│    │                                                              │  │
│    │ Returns structured AIResponse:                               │  │
│    │ {                                                            │  │
│    │   "summary": "User asking about machine learning",           │  │
│    │   "sentiment": 50,                                           │  │
│    │   "response": "Machine learning is a subset of AI..."        │  │
│    │ }                                                            │  │
│    └──────────────────────┬───────────────────────────────────────┘  │
│                           ↓                                          │
└───────────────────────────┼──────────────────────────────────────────┘
                            │ Returns to Flask
                            ↓
┌───────────────────────────┼──────────────────────────────────────────┐
│ 6. FLASK SERVER (continued - app.py)                                 │
│    Receives AIResponse from model.py                                │
│    Calculates: duration = current_time - start_time                 │
│    Adds to result: result['duration'] = 11.81 seconds               │
│    Logs: "Generated response in 11.81 seconds"                      │
│                                                                      │
│    Final response object:                                           │
│    {                                                                │
│      "summary": "User asking about machine learning",               │
│      "sentiment": 50,                                               │
│      "response": "Machine learning is a subset of AI...",           │
│      "duration": 11.81                                              │
│    }                                                                │
└───────────────────────────┬──────────────────────────────────────────┘
                            │ return jsonify(result)
                            ↓
┌───────────────────────────┼──────────────────────────────────────────┐
│ 7. BROWSER (JavaScript - static/script.js)                          │
│    Receives JSON response                                           │
│    Updates UI:                                                      │
│    - Hides loading indicator                                        │
│    - Displays summary                                               │
│    - Shows sentiment score (0-100)                                  │
│    - Displays AI response                                           │
│    - Shows response time: "Qwen took 11.81 seconds"                 │
│    - User can send next message                                     │
│                                                                      │
│    Chat now shows:                                                  │
│    You: "What is machine learning?"                                 │
│    Qwen: [Summary, sentiment, response, time]                       │
└────────────────────────────────────────────────────────────────────┘
```

---

### **Step-by-Step Breakdown**

#### **When Browser Sends Message:**
```
1. JavaScript captures user input
2. Sends POST to /generate with message and model
3. Shows loading indicator (animated dots)
```

#### **When Flask Receives Request:**
```
1. Validates message is not empty
2. Validates model is 'qwen'
3. Defines system prompt (instructions for Qwen)
4. Records start time
5. Calls qwen_response() from model.py
```

#### **When LangChain Processes:**
```
1. PromptTemplate formats with Qwen special tokens
2. OllamaLLM sends to Ollama server
3. JsonOutputParser validates response structure
4. Returns AIResponse object
```

#### **When Ollama Runs Qwen:**
```
1. Loads model into GPU/CPU memory
2. Tokenizes input text
3. Converts tokens to embeddings (vectors)
4. Runs through 32 transformer layers
5. Iteratively predicts next token
6. Continues until max_tokens reached or natural stop
7. Returns complete response
```

#### **When Flask Returns Response:**
```
1. Calculates elapsed time
2. Adds duration to response
3. Logs processing time
4. Returns JSON to browser
```

#### **When Browser Displays:**
```
1. JavaScript receives JSON
2. Hides loading indicator
3. Adds message to chat history
4. Displays summary, sentiment, response
5. Shows response time
6. Auto-scrolls to latest message
7. Clears input field
8. Focuses input for next message
```

---

### **Key Timings**

```
Network request:      < 1ms
Flask validation:     < 1ms
LangChain setup:      < 1ms
Ollama processing:    10-15 seconds ⏰ (most time here)
JsonOutputParser:     < 1ms
Flask response:       < 1ms
Browser display:      < 100ms

Total:                ~11-15 seconds
```

---

### **Error Flow Example**

If something goes wrong:

```
Browser sends empty message ("")
          ↓
Flask catches: if not user_message
          ↓
Returns: {"error": "Message cannot be empty"}, 400
          ↓
Browser receives error
          ↓
JavaScript catches and displays error message
          ↓
User can try again
```

---

### **Configuration Impact**

Same message, different config:

```
Config 1: temperature=0.3, max_tokens=256
Message: "Hello"
Response: "Hello! How can I assist you today?"
Duration: 11.81s
Next time same message: Same response (deterministic)

Config 2: temperature=0.9, max_tokens=256
Message: "Hello"
Response: "Hey there! How may I help you?"
Duration: 12.15s
Next time same message: Different response (creative)

Config 3: temperature=0.3, max_tokens=50
Message: "Hello"
Response: "Hello! How can..." (cut off)
Duration: 8.2s (faster, shorter)
```

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