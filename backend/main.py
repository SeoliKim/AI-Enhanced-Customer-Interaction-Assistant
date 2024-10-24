import uuid
from langchain_openai import ChatOpenAI
from config.config import Config
from tools.order_tracking import track_order
from tools.product_recommendations import get_product_recommendations
from assistant.prompt import assistant_prompt
from assistant.assistant import Assistant
from assistant.graph import create_customer_support_graph

def main():
    llm = ChatOpenAI(model=Config.MODEL_NAME, temperature=Config.TEMPERATURE)
    
    tools = [track_order, get_product_recommendations]
    assistant_runnable = assistant_prompt | llm.bind_tools(tools)
    assistant = Assistant(assistant_runnable)
    
    graph = create_customer_support_graph(assistant, tools)
    
    print("Customer Service Assistant Ready! (Type 'quit' to exit)")
    print("-" * 50)
    
    thread_id = str(uuid.uuid4())
    config = {
        "configurable": {
            "user_id": Config.DEFAULT_USER,
            "thread_id": thread_id,
            "checkpoint_ns": "customer_service",
            "checkpoint_id": str(uuid.uuid4())
        }
    }
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'quit':
            break
            
        response = graph.invoke({
            "messages": [("user", user_input)]
        }, config)
        
        print("\nAssistant:", end=" ")
        for message in response["messages"]:
            if hasattr(message, 'content'):
                print(message.content)
            elif isinstance(message, tuple) and len(message) == 2:
                print(message[1])

if __name__ == "__main__":
    main()