import textwrap
import sys

from core.ai_service import answer_question

def display_menu():
    """Display the menu"""
    print("\n" + "-"*50)
    print("REVIEWER".center(50))
    print("-"*50)
    print("[1] Create Summary and Bullet Points")
    print("[2] Ask Questions About the Document")
    print("[3] Exit")
    while True:
        try:
            choice = int(input("\nEnter your choice (1-3): "))
            if 1 <= choice <= 3:
                return choice
            print("Invalid choice. Please enter a number between 1 and 3.")
        except ValueError:
            print("Please enter a valid number.")

def display_qa_menu():
    """Display the question-answer mode."""
    print("\n"+"-"*50)
    print("Question - Answer".center(50))
    print("-"*50)
    print("Type your question or use one of these commands:")
    print("  'help' - Show this help message")
    print("  'back' or 'menu' - Return to main menu")
    print("  'exit' - Exit the program")

def handle_qa_mode(document_text):
    """Handle the question-answering mode with navigation and context/conversation memory."""
    display_qa_menu()

    conversation_history = []
    
    while True:
        question = input("\nAsk a question: ").strip()
        
        # Handle commands
        if question.lower() in ['back', 'menu']:
            print("\nReturning to menu...")
            return
        elif question.lower() == 'exit':
            print("\nExiting program.. Goodbye!")
            sys.exit(0)
        elif question.lower() == 'help':
            display_qa_menu()
            continue
        elif not question:
            print("Please enter a question or command.")
            continue
        
        # Process question
        print("\nThinking...")
        try:
            answer = answer_question(document_text, question, conversation_history)

            # add to conversation history (last 5 interactions)
            conversation_history.append({"question": question, "answer": answer})
            if len(conversation_history) > 5:
                conversation_history.pop(0)
            
            print("\nAnswer:")
            # Print the answer with proper wrapping
            for line in textwrap.wrap(str(answer), width=80):
                print(line)
                
            print("\n" + "-"*50)
            print("Type another question, 'back' for menu, or 'help' for options")
            
        except Exception as e:
            print(f"\nError processing question: {e}")
            print("You can try another question or type 'back' to return to the menu")
