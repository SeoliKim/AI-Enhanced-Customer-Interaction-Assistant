from typing import Annotated, TypedDict
from langchain_core.messages import HumanMessage
from langchain_community.llms import LlamaCpp
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.runnables import RunnableSequence
#from order_tracking import create_order_tracking_agent

class AgentState(TypedDict):
    messages: Annotated[list[HumanMessage], "The messages in the conversation"]
    next_agent: Annotated[str, "The next agent to call"]


class RouterAgent:
    def __init__(self):
        self.llm = LlamaCpp(model_path='../llama-2-7b.Q4_K_M.gguf', temperature=0.1)
        self.prompt = PromptTemplate(
            input_variables=["query"],
            template="""INSTRUCTION: Classify the following user query into EXACTLY ONE of these categories:
- OrderTrackingAgent
- ProductRecommendationAgent
- VisualSearchAgent

User Query: {query}

IMPORTANT: Your entire response must be ONLY ONE of the above category names. Do not include any other text.

Classification:"""
        )
        self.chain = RunnableSequence(self.prompt | self.llm)

    def route(self, state: AgentState) -> str:
        human_message = state["messages"][-1]
        print({human_message.content})
        response = self.chain.invoke({"query": human_message.content})
        print(f"Debug - Raw LLM response: {response}")
        
        #agent_name = self.parse_response(response)
        #print(f"Debug - Parsed agent name: {agent_name}")
        #return response
        return response  # Return the raw LLM response

    def parse_response(self, response: str) -> str:
        response = response.strip().lower()
        if "ordertrackingagent" in response:
            return "order_tracking"
        elif "productrecommendationagent" in response:
            return "product_recommendation"
        elif "visualsearchagent" in response:
            return "visual_search"
        else:
            return "router"
        


def create_router():
    return RouterAgent()



# Example usage
if __name__ == "__main__":
    router = create_router()
    state = AgentState(messages=[HumanMessage(content="What's the status of my order?")], next_agent="")
    final_state = router.route(state)
    print(f"Routed to: {final_state['next_agent']}")