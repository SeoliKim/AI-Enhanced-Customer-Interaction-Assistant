from langchain_anthropic import ChatAnthropic
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.chat_models import ChatLlamaCpp
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableConfig
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from typing import Annotated, Literal
from typing_extensions import TypedDict
from langgraph.graph.message import AnyMessage, add_messages
from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableLambda
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver

from langgraph.graph import END, StateGraph, START, MessagesState

from backend.assistant.tools import order_tracking, product_recommandation, create_tool_node_with_fallback


class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


system = """<<SYS>>
You are a helpful, friendly, polite and honest customer support assistant for a e-commerce platform
Use the provided tools to assist in order tracking or recommand product.
IMPORTANT: Your entire response is based on ToolMessgae. Do not makeup a product or state of order.
Reply to user after every tool call
<</SYS>>"""

# examples = [
#     HumanMessage(
#         "I want to buy a new phone", name="example_user"
#     ),
#     AIMessage(
#         "",
#         name="example_assistant",
#         tool_calls=[
#             {"name": "get_product_recommandation", "args": {"item": "phone"},"id": "1"}
#         ],
#     ),
#     ToolMessage("iphone 16 with id 123123123", tool_call_id="1"),
#     AIMessage(
#         "Hello! Sure, I can help with that. I recommend Iphone 16 with id 123123123. Let me know if you would like another recommandation",
#         name="example_assistant",
#     ),
# ]

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "{messages}"),
    ]
)

tools = [order_tracking, product_recommandation]

class Assistant:
    def __init__(self):
        self.llm = ChatLlamaCpp(model_path='../llama-2-7b.Q4_K_M.gguf', temperature=0,
                                top_p=1,
                                n_ctx=16000, stop=['### Human:', '### Assistant:', '### Tool Calls:'])
        self.runnable = prompt | self.llm.bind_tools(
            tools=tools,
            tool_choice={"type": "function", "function": {"name": "get_order_tracking", "description": "retrive state of the order.", },
                         "type": "function", "function": {"name": "get_product_recommandation", "description": "recommand a product"}},
        )

    def __call__(self, state: State, config: RunnableConfig):
        while True:
            configuration = config.get("configurable", {})
            customer_id = configuration.get("customer_id", None)
            state = {**state, "user_info": customer_id}
            result = self.runnable.invoke(state)
            # If the LLM happens to return an empty response, we will re-prompt it
            # for an actual response.
            if not result.tool_calls and (
                not result.content
                or isinstance(result.content, list)
                and not result.content[0].get("text")
            ):
                messages = state["messages"] + \
                    [("user", "Respond with a real output.")]
                state = {**state, "messages": messages}
            else:
                break
        return {"messages": result}

    
    def create_graph(self):
        # Define the function that determines whether to continue or not
        graph = StateGraph(State)
        # Define nodes: these do the work
        graph.add_node("assistant", self)
        graph.add_node("tools", create_tool_node_with_fallback(tools))

        # Define edges: these determine how the control flow moves
        graph.add_edge(START, "assistant")
        graph.add_conditional_edges(
            "assistant",
            tools_condition,
        )
        graph.add_edge("tools", "assistant")
        # The checkpointer lets the graph persist its state
        # this is a complete memory for the entire graph.
        memory = MemorySaver()
        return graph.compile(checkpointer=memory)
