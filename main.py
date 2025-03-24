#!/usr/bin/env python3

import os
import sys
from dotenv import load_dotenv
import pyfiglet

from config.settings import initialize_settings
from core.document_processor import process_file
from core.cli import display_menu, display_qa_menu, handle_qa_mode
from core.text_chunker import chunk_text
from core.ai_service import summarize_text_to_bullets
from utils.file_helpers import get_file_path

def main():
    try:
        print("\n"+pyfiglet.figlet_format("REVIEWER", "slant"))
        print("Welcome to Reviewer!")
        
        # Load environment variables and initialize settings
        load_dotenv()
        initialize_settings()
        
        file_path = get_file_path()
        
        # Extract the text
        print("\nProcessing file, please wait...")
        document_text = process_file(file_path)
        print("File processed successfully!")
        
        while True:
            choice = display_menu()
            
            if choice == 1:
                print("\nGenerating summary and bullet points, please wait...")
                result = summarize_text_to_bullets(document_text)
                print("\n" + "-"*50)
                print("Summary and Key Points".center(50))
                print("-"*50)
                print(result)
                
            elif choice == 2:
                handle_qa_mode(document_text)
            
            elif choice == 3:
                print("\nExiting program.. Goodbye!")
                break
    
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user during initialization")
        sys.exit(0)
