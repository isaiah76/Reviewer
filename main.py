import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from PyPDF2 import PdfReader

# Load environment variables from .env file
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

if not google_api_key:
    raise ValueError("Google API key is not set in the environment variables.")

# Initialize the Gemini model
llm = GoogleGenerativeAI(model="gemini-pro")

# Define the prompt template
prompt_template = """
Given the following text from a study document, extract the key points and create a concise summary and bullet points for an examination reviewer about this.

Text:
{text}

Summary:

bullet points:
"""

# Initialize the PromptTemplate and LLMChain
prompt = PromptTemplate(input_variables=["text"], template=prompt_template)
summarization_chain = LLMChain(prompt=prompt, llm=llm)

def extract_text_from_pdf(pdf_path):
    """Extract text from each page of the PDF."""
    pdf_text = []
    try:
        with open(pdf_path, "rb") as file:
            reader = PdfReader(file)
            for page in reader.pages:
                text = page.extract_text()
                if text:  # Check if text extraction was successful
                    pdf_text.append(text)
    except Exception as e:
        raise IOError(f"Error reading the PDF file: {e}")
    return " ".join(pdf_text)  # Join the list into a single string

def summarize_text_to_bullets(pdf_text):
    """Summarize the extracted text into bullet points using the LLM."""
    response = summarization_chain.run(text=pdf_text)
    return response

def pdf_to_bullet_summary(pdf_path):
    """Main function to extract and summarize PDF content."""
    pdf_text = extract_text_from_pdf(pdf_path)
    bullet_summary = summarize_text_to_bullets(pdf_text)
    return bullet_summary

if __name__ == "__main__":
    pdf_path = "./test.pdf"
    try:
        review_notes = pdf_to_bullet_summary(pdf_path)
        print("Review Notes:\n", review_notes)
    except Exception as e:
        print(f"An error occurred: {e}")

