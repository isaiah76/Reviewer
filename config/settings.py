import os
import pytesseract
from google.generativeai.types.safety_types import HarmCategory, HarmBlockThreshold

# Model configuration
GEMINI_MODEL_TEXT = "gemini-2.0-flash"  
GEMINI_TEMPERATURE = 0.5
GEMINI_MAX_OUTPUT_TOKENS = 2048
GEMINI_SAFETY_SETTINGS = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
}

# System prompts
SUMMARY_SYSTEM_PROMPT = """
You are an expert study assistant. Extract key points from educational materials and create concise, 
well-structured summaries that are easy to understand and remember. 

IMPORTANT: Your primary task is to identify and highlight the MOST critical information. 
For each topic, clearly indicate which points are essential for exams or understanding core concepts,
using phrases like "CRITICAL:", "KEY CONCEPT:", or "EXAM FOCUS:" before the most important points.

Organize information by importance, with the most crucial concepts first. Use clear formatting 
to make important distinctions obvious.
"""

QA_SYSTEM_PROMPT = """
You are an expert tutor. Your task is to answer questions about educational materials clearly and accurately. 

When provided with conversation history, use it to understand the context of the current question. If the user refers to something discussed earlier, maintain continuity in your responses. 
"""

# Text chunking settings (for context window)
MAX_CHUNK_SIZE = 30000

# Supported file formats
SUPPORTED_FILE_FORMATS = {
    '.pdf': 'PDF Document',
    '.pptx': 'PowerPoint Document',
    '.ppt': 'Legacy PowerPoint Document (Limited Support)'
}

def initialize_settings():
    """Initialize any settings that need runtime configuration"""
    # Set Tesseract OCR path if specified in environment
    tesseract_cmd = os.getenv("TESSERACT_CMD")
    if tesseract_cmd:
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
    
    # Validate API keys
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("Gemini API key is not set in the environment variables.")
