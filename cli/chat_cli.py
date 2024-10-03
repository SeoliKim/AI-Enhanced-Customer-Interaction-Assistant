import sys
import os
# Add the parent directory to the Python path to import from backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.main import CustomerAssistant


def test_router():
    assistant = CustomerAssistant()
    while True:
        user_input = input("Custumer: ")
        if user_input.lower() == 'quit':
            break

        try:
            user_input= user_input 
            response = assistant.process_user_input(user_input)
            #print(f"Agent: {response}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        

    print("Thank you for using the Customer Assistant Chatbot!")


def response_generator_test():
    print("testing response generator...")
    
    def create_testing_case():
        agent_map= {1: "order_tracking", 2: "product_recommendation", 3: "image analysis", 4: "inquiry"}
        while True:
            print("Select the previous agent for the response")
            print("1: order tracking")
            print("2: product recommandation")
            print("3: image analysis")
            print("4: inquiry")
            try:
                a = int(input("Enter: "))
                if a in range(1, 5):
                    message = input("Enter specific output message: ")
                    return (agent_map[a], message )
                else:
                    print("Invalid input. Please enter a number between 1 and 4.")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 4.")
        
    def select_testing_case():
        test_cases= [
            ("order_tracking","order 1234 has delivered"),
            ("order_tracking","missing order ID",),
            ("order_tracking", "Order ID doesn't exist in database"),
            ("product_recommendation", "recommand Stanley Quencher H2.0 FlowState Stainless Steel Vacuum Insulated Tumbler with Lid and Straw, 30oz",),
            ("product_recommendation", "no recommandation",),
            ("image","couldn't recognized the provided image",),
            ("router", "my cup is missing"),
            ("router", "fsidjfnsdjklfnfjds"),
        ]
        while True:
            print("Test cases:")
            for i, tc in enumerate(test_cases):
                print(str(i), ":", tc)
            print("enter the number for selected test case")
            try:
                i = int(input("Select Test case: "))
                if i in range(0, len(test_cases)):
                    return test_cases[i]
                else:
                    print("Invalid input.")
            except ValueError:
                print("Invalid input.")
    
    test_case=""
    while True:
        print("enter 0 to use example test cases")
        print("enter 1 to custum test case")
        try:
            response_type = int(input("Response type: "))
            if response_type == 0:
                print("enter the number for selected test case")
                test_case= select_testing_case()
                break
        
            if response_type == 1:
                test_case= create_testing_case()
                break
        except ValueError:
            print("Invalid input.")
 
    assistant = CustomerAssistant()
    response = assistant.generate_response(test_case[0], test_case[1])
    print("Agent response: "+response)
    
def test_assistant():
    print("testing assistant...")
    print("type 'quit' to exit.")
     
    assistant = CustomerAssistant()
    assistant_graph= assistant.create_assistant_graph()
    
    thread_id = str(123123123)

    config = {
        "configurable": {
        "customer_id": "1234",
        # Checkpoints are accessed by thread_id
        "thread_id": thread_id,
        }
    }

    _printed = set()
    while True:
        user_input = input("Custumer: ")
        if user_input.lower() == 'quit':
            break
        events = assistant_graph.stream(
            {"messages": ("user", user_input)}, config, stream_mode="values"
        )
        for event in events:
            _print_event(event, _printed)

def _print_event(event: dict, _printed: set, max_length=1500):
    current_state = event.get("dialog_state")
    if current_state:
        print("Currently in: ", current_state[-1])
    message = event.get("messages")
    if message:
        if isinstance(message, list):
            message = message[-1]
        if message.id not in _printed:
            msg_repr = message.pretty_repr(html=True)
            if len(msg_repr) > max_length:
                msg_repr = msg_repr[:max_length] + " ... (truncated)"
            print(msg_repr)
            _printed.add(message.id)
 
# run agent unit test
def main():
    print("Welcome to the Customer Assistant Chatbot!")
    print("Type 'quit' to exit.")
    
    def select_testing_agent():
        while True:
            print("Choose the testing agent.")
            print("1 router")
            print("2 assistant")
            try:
                choice = int(input("Select the agent: "))
                if choice in range(1, 3):
                    return int(choice)
                else:
                    print("Invalid input. Please enter 1 or 2.")
            except ValueError:
                print("Invalid input. Please enter 1 or 2.")
    choice = select_testing_agent()
    match choice:
        case 1:
             test_router()
        case 2:
             test_assistant()
        case _:
            print("No matching agent")           
    
    
        
 

    
    


if __name__ == "__main__":
    main()
   