from backend.agents.router import create_router, AgentState
from backend.agents.order_tracking import create_order_tracking_agent
from backend.agents.response_generator import create_response_generator
from backend.assistant.assistant import Assistant
from langchain_core.messages import HumanMessage, AIMessage

    
class CustomerAssistant:
    def __init__(self):
        self.router = create_router()
        self.order_tracking = create_order_tracking_agent()
        # self.response_generator = create_response_generator()
        # Initialize other agents here (we'll implement these later)
        # self.product_recommendation = ProductRecommendationAgent()
        # self.visual_search = VisualSearchAgent()
        
    def process_user_input(self, user_input: str) -> str:
        state = AgentState(messages=[HumanMessage(content=user_input)], next_agent="router")
        
        while True:
            if state["next_agent"] == "router":
                llm_response = self.router.route(state)
                next_agent = self.router.parse_response(llm_response)
                
                if next_agent != "order_tracking":
                    return f"This query would be handled by the {next_agent} agent."
                state["next_agent"] = next_agent
            
            elif state["next_agent"] == "order_tracking":
                state = self.order_tracking.process_query(state)
                ai_message = state["messages"][-1]
                print("Agent:", ai_message.content)
                
                if state["next_agent"] == "router":
                    return ai_message.content
                elif state["next_agent"] == "order_tracking":
                    user_input = input("You: ")
                    state["messages"].append(HumanMessage(content=user_input))
            
            else:
                return f"Unhandled agent: {state['next_agent']}"
    
    def create_assistant_graph(self):
        assistant = Assistant()
        assistant_graph= assistant.create_graph()
        return assistant_graph
        

# Example usage
if __name__ == "__main__":
    assistant = CustomerAssistant()
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break
        response = assistant.process_user_input(user_input)
        print("Agent:", response)


