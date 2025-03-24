import os
import sys
from config.settings import SUPPORTED_FILE_FORMATS

def is_valid_file(path):
    """Check if the path exists and has a supported extension."""
    if not os.path.exists(path):
        print(f"Error: File '{path}' does not exist")
        return False
    
    file_ext = os.path.splitext(path)[1].lower()
    if file_ext not in SUPPORTED_FILE_FORMATS:
        print(f"Error: Unsupported file format. Supported formats are:")
        for ext, desc in SUPPORTED_FILE_FORMATS.items():
            print(f"  {ext} - {desc}")
        return False
    return True

def get_file_path():
    """Get file path from command line argument or user input."""
    # Check cli
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if is_valid_file(file_path):
            return file_path
        sys.exit(1)  # if argument is invalid
    
    # prompt for input
    while True:
        file_path = input("\nPlease enter the path to your file (.pdf, .pptx, or .ppt): ").strip()
        if file_path.lower() == 'exit':
            print("Exiting program...")
            sys.exit(0)
        if is_valid_file(file_path):
            return file_path
        print("\nTry again or type 'exit' to quit")
