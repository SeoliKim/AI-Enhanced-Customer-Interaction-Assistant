import sys
import os

# Add the parent directory to the Python path to import from backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.main import CustomerAssistant

def main():
    assistant = CustomerAssistant()
    print("Welcome to the Customer Assistant Chatbot! How may I help you?")
    print("Type 'quit' to exit.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break

        try:
            response = assistant.process_user_input(user_input)
            #print(f"Agent: {response}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        

    print("Thank you for using the Customer Assistant Chatbot!")

if __name__ == "__main__":
    main()
