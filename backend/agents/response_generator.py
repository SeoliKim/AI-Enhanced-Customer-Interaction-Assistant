from typing import Annotated, TypedDict
from langchain_core.messages import HumanMessage
from langchain_community.llms import LlamaCpp
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.runnables import RunnableSequence
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate


# class ResponseState(TypedDict):
#     inputs: Annotated[list[HumanMessage],
#                       "The user messages in the conversation"]
#     outputs: Annotated[list[], "The agent output based on user message"]
#     prev_agents: Annotated[str, "Agent that send the input"]

# common contexts for different agent output
contexts = {
    "order_tracking": """
    Please assist with order tracking for a customer. 

    1. Explain to the user about state of order if provided in output
    2. For missing information, ask for it. 
    3. If the issue is resolved, confirm with the customer and ask if they need any further assistance or would like a product recommendation based on their order.
    """,
    "product_recommendation": """
    Please assist the customer with product recommendations.

    1. Explain why the product is recommanded for user 
    2. Confirm with the customer if they are satisfied with the recommendation or if they would like to explore additional options.
    3. End the conversation politely, ensuring customer satisfaction.
    """,
    "router": """
    Please assist the customer by first understanding their needs.

    1. Greet the customer warmly and ask how you can assist them today.
    2. Listen carefully to the customer's response to determine whether they need help with order tracking, product recommendations, or image analysis.
    - if none helps the custumer, apologize for the incovinience
    3. If there’s any confusion or an error in understanding the customer’s request, politely ask for clarification to ensure you provide the correct assistance.
    4. End the conversation politely, ensuring the customer is satisfied with the assistance provided.
    """,
    
}


order_examples = [
    {"input": "Order with ID 1234 has delivered", "output": "Great news! Your order with ID 1234 has been delivered. If you have any issues with your package, please let us know."},
    {"input": "Order ID 1234 doesn't exist in database", "output": "I apologize, but I couldn't find order ID 1234 in our system. Could you double-check the number and try again?"},
    {"input": "Delayed shipment", "output": "We're sorry, but your order is slightly delayed. We're working to ship it as soon as possible and will update you with a new delivery date."},
    {"input": "missing order id", "output": "To check your order status, I'll need your order ID. Once you provide it, I can give you the latest update on your package."},
]

example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{input}"),
        ("ai", "{output}"),
    ]
)

order_few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=order_examples,
)

order_final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful, friendly, polite and honest customer support assistant. If a question does not make any sense, or is not factually coherent, explain why instead of answering something incorrect. If you don't know the answer to a question, please don't share false information.Use the provided context to write an appropriate 1-3 senetnce response to the custumer. "),
        order_few_shot_prompt,
        ("human", "{input}"),
    ]
)

response_agent_prompt = PromptTemplate(
    input_variables=["context"],
    template= """
    <s>[INST] <<SYS>>
    You are a helpful, friendly, polite and honest customer support assistant.
    If a question does not make any sense, or is not factually coherent, explain why instead of answering something incorrect.
    If you don't know the answer to a question, please don't share false information.
    <</SYS>>
    
    
    
    CONTEXT: {context}
    """
)


class ResponseAgent:
    def __init__(self):
        self.llm = LlamaCpp(
            model_path='../llama-2-7b.Q4_K_M.gguf', temperature=0.1)
        self.prompt = order_final_prompt
        self.chain = RunnableSequence(self.prompt | self.llm)

    def generate_response(self, prev_agent:str, output_text:str, ) -> str:
        print("generating response based on", "prev agent:", prev_agent, "user message:", output_text, "...")
        
        # check if value for prev_agent is valid
        if prev_agent not in contexts:
            print("prev agent is not valid")
            return 

        response = self.chain.invoke(
            {"input": output_text})
        
    
        print(f"Debug - Raw LLM response: {response}")

        # agent_name = self.parse_response(response)
        # print(f"Debug - Parsed agent name: {agent_name}")
        # return response
        return response  # Return the raw LLM response


def create_response_generator():
    return ResponseAgent()


# Example usage
if __name__ == "__main__":
    response_generator = create_response_generator()
    state = AgentState(messages=[HumanMessage(
        content="What's the status of my order?")], next_agent="")
    final_state = response_generator.route(state)
    print(f"Routed to: {final_state['next_agent']}")
