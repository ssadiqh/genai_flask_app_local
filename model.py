# AI Model Integration using LangChain with Local Qwen
# This replaces IBM Watsonx integration with local Ollama/Qwen

from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from config import PARAMETERS, CREDENTIALS, QWEN_MODEL

# ============================================
# 1. Define JSON Output Structure
# ============================================
class AIResponse(BaseModel):
    """Structured response format from AI"""
    summary: str = Field(description="Summary of the user's message")
    sentiment: int = Field(description="Sentiment score from 0 (negative) to 100 (positive)")
    response: str = Field(description="Suggested response to the user")

# ============================================
# 2. Initialize JSON Parser
# ============================================
json_parser = JsonOutputParser(pydantic_object=AIResponse)

# ============================================
# 3. Initialize Local Qwen Model
# ============================================
def initialize_qwen_model():
    """Initialize connection to local Qwen model via Ollama"""
    return OllamaLLM(
        model=QWEN_MODEL,
        base_url=CREDENTIALS["base_url"],
        temperature=PARAMETERS["temperature"],
        num_predict=PARAMETERS["max_tokens"]
    )

qwen_llm = initialize_qwen_model()

# ============================================
# 4. Define Prompt Template for Qwen
# ============================================
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

# ============================================
# 5. Main Response Function
# ============================================
def get_ai_response(model, template, system_prompt, user_prompt):
    """
    Chain together prompt template, model, and JSON parser

    Flow: Template -> Model -> JSON Parser
    """
    chain = template | model | json_parser
    return chain.invoke({
        'system_prompt': system_prompt,
        'user_prompt': user_prompt,
        'format_prompt': json_parser.get_format_instructions()
    })

# ============================================
# 6. Public API Function
# ============================================
def qwen_response(system_prompt, user_prompt):
    """
    Get structured JSON response from local Qwen model

    Args:
        system_prompt: Instructions for the AI
        user_prompt: User's question/message

    Returns:
        Structured AIResponse object (dict) with summary, sentiment, response
    """
    return get_ai_response(qwen_llm, qwen_template, system_prompt, user_prompt)