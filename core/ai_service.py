import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage

from config.settings import (
    GEMINI_MODEL_TEXT,
    GEMINI_TEMPERATURE,
    GEMINI_MAX_OUTPUT_TOKENS,
    GEMINI_SAFETY_SETTINGS,
    SUMMARY_SYSTEM_PROMPT,
    QA_SYSTEM_PROMPT
)
from core.text_chunker import chunk_text

model = None

def initialize_model():
    """Initialize the LLM model."""
    global model
    if model is None:
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        model = ChatGoogleGenerativeAI(
            model=GEMINI_MODEL_TEXT,
            google_api_key=gemini_api_key,
            temperature=GEMINI_TEMPERATURE,
            max_output_tokens=GEMINI_MAX_OUTPUT_TOKENS,
            safety_settings=GEMINI_SAFETY_SETTINGS
        )
    return model

def summarize_text_to_bullets(text):
    """Summarize the extracted text into bullet points."""
    # Initialize the model if not already done
    initialize_model()
    
    # check if text needs to be chunked
    chunks = chunk_text(text)
    
    if len(chunks) > 1:
        print(f"\nContent is large, processing in {len(chunks)} parts...")
        all_summaries = []
        
        for i, chunk in enumerate(chunks, 1):
            print(f"Processing part {i}/{len(chunks)}...")
            # create messages for the chat model
            messages = [
                SystemMessage(content=SUMMARY_SYSTEM_PROMPT),
                HumanMessage(content=f"""
Given the following text (part {i} of {len(chunks)}) from a study document, extract the key points and create a concise summary and bullet points for an examination reviewer about this part.
Text:
{chunk}
Please format your response exactly as follows:
Summary:
[A brief overview of the main topics and key concepts]
Bullet Points:
• [Key point 1]
• [Key point 2]
• [Key point 3]
...and so on
Do not use any other formatting, just plain bullet points and text.
""")
            ]
            
            # generate response
            response = model.invoke(messages)
            all_summaries.append(response.content)
        
        # If we have multiple chunks, combine the summaries
        if len(all_summaries) > 1:
            combined_text = "\n\n".join(all_summaries)
            
            # create a final combined summary
            messages = [
                SystemMessage(content=SUMMARY_SYSTEM_PROMPT),
                HumanMessage(content=f"""
Given the following summaries from different parts of a document, combine them into one coherent summary and bullet point list:
{combined_text}
Please format your response exactly as follows:
Summary:
[A brief overview of the main topics and key concepts]
Bullet Points:
• [Key point 1]
• [Key point 2]
• [Key point 3]
...and so on
Do not use any other formatting, just plain bullet points and text.
""")
            ]
            
            # Generate combined response
            response = model.invoke(messages)
            return response.content
        else:
            return all_summaries[0]
    else:
        # If the text doesn't need chunking, process it as normal
        messages = [
            SystemMessage(content=SUMMARY_SYSTEM_PROMPT),
            HumanMessage(content=f"""
Given the following text from a study document, extract the key points and create a concise summary and bullet points for an examination reviewer about this.
Text:
{text}
Please format your response exactly as follows:
Summary:
[A brief overview of the main topics and key concepts]
Bullet Points:
• [Key point 1]
• [Key point 2]
• [Key point 3]
...and so on
Do not use any other formatting, just plain bullet points and text.
""")
        ]
        
        # generate response
        response = model.invoke(messages)
        return response.content

def answer_question(text, question, conversation_history):
    """Answer a question based on the document content and conversation context"""
    # Initialize the model if not already done
    initialize_model()
    
    # conversation context 
    conversation_context = ""
    if len(conversation_history) > 0:
        conversation_context = "Previous conversation:\n"
        for i, exchange in enumerate(conversation_history, 1):
            conversation_context += f"Question {i}: {exchange['question']}\n"
            conversation_context += f"Answer {i}: {exchange['answer']}\n\n"

    # check if text needs to be chunked
    chunks = chunk_text(text)
    
    if len(chunks) > 1:
        print(f"\nContent is large, searching across {len(chunks)} sections...")
        all_answers = []
        
        for i, chunk in enumerate(chunks, 1):
            # create the messages for the chat model
            messages = [
                SystemMessage(content=QA_SYSTEM_PROMPT),
                HumanMessage(content=f"""
Given the following text (section {i} of {len(chunks)}) and a question, provide an answer 

{conversation_context}
Text:
{chunk}

Current Question:
{question}

If this section contains relevant information to the question, answer it directly and concisely. 
If the question refers to previous questions or answers, use the conversation context to understand what the user is asking.
If the answer cannot be determined from this section, simply state "No relevant information found in this section."
""")
            ]
            
            # generate response
            response = model.invoke(messages)
            if "No relevant information found in this section" not in response.content:
                all_answers.append(response.content)
        
        # If we found answers in multiple chunks, combine them
        if all_answers:
            if len(all_answers) > 1:
                combined_answers = "\n\n".join([f"Answer from section {i+1}:\n{answer}" for i, answer in enumerate(all_answers)])
                
                # final combined answer
                messages = [
                    SystemMessage(content=QA_SYSTEM_PROMPT),
                    HumanMessage(content=f"""
I found multiple relevant sections in the document that might answer your question. Here are the answers from each section:

{conversation_context}
{combined_answers}

Current Question:
{question}

Please combine these answers into one comprehensive response, removing any contradictions or redundancies. 
If the answers provide different perspectives, include all relevant viewpoints.
If the question refers to previous questions or answers, use the conversation context to provide continuity.
""")
                ]
                
                # generate combined response
                response = model.invoke(messages)
                return response.content
            else:
                return all_answers[0]
        else:
            return "I couldn't find information relevant to your question in the document."
    else:
        # If the text doesnt need chunking, process it as normal
        messages = [
            SystemMessage(content=QA_SYSTEM_PROMPT),
            HumanMessage(content=f"""
Given the following text and a question, provide a comprehensive and accurate answer based solely on the information in the text.

{conversation_context}
Text:
{text}

Current Question:
{question}

Answer the question directly and concisely
If the question refers to previous questions or answers, use the conversation context to provide continuity and context-aware responses.
If the answer cannot be determined from the text, state that clearly.
""")
        ]
        
        # generate response
        response = model.invoke(messages)
        return response.content
