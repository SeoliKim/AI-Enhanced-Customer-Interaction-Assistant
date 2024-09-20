from backend.agents.router import create_router, AgentState
from langchain_core.messages import HumanMessage

class CustomerAssistant:
    def __init__(self):
        self.router = create_router()
        # Initialize other agents here (we'll implement these later)
        # self.order_tracking = OrderTrackingAgent()
        # self.product_recommendation = ProductRecommendationAgent()
        # self.visual_search = VisualSearchAgent()


    def process_user_input(self, user_input: str) -> str:
        initial_state = AgentState(messages=[HumanMessage(content=user_input)], next_agent="")
        response = self.router.route(initial_state)
        print (f"This query would be handled by the {response}")
        return response
    
# Example usage
if __name__ == "__main__":
    assistant = CustomerAssistant()
    print(assistant.process_user_input("What's the status of my order?"))
    print(assistant.process_user_input("Can you recommend a good laptop?"))
    print(assistant.process_user_input("Find a red t-shirt in this image"))