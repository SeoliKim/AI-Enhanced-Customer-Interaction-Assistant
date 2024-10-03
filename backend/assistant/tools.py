from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableLambda, Runnable, RunnableConfig
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from langgraph.prebuilt import ToolNode

class OrderInput(BaseModel):
    id: str = Field(description="id, sequence of number. ie.12332786432")
    
# temporary tool simulation
@tool("get_order_tracking", args_schema=OrderInput)
def order_tracking(id: str) -> str:
    '''retrive state of the order, ie. delivered'''
    res= input(f"Enter order tracking result for {id}")
    return res

class ProductInput(BaseModel):
    item: str = Field(description="name of a product, ie.mirror, phone")
    
# temporary tool simulation
@tool("get_product_recommandation", args_schema=ProductInput)
def product_recommandation(item: str ) -> str:
    '''recommand a product'''
    res= input(f"Enter product recommandation result for {item}: ")
    return res

def handle_tool_error(state) -> dict:
    error = state.get("error")
    tool_calls = state["messages"][-1].tool_calls
    return {
        "messages": [
            ToolMessage(
                content=f"Error: {repr(error)}\n please fix your mistakes.",
                tool_call_id=tc["id"],
            )
            for tc in tool_calls
        ]
    }

def create_tool_node_with_fallback(tools: list) -> dict:
    return ToolNode(tools).with_fallbacks(
        [RunnableLambda(handle_tool_error)], exception_key="error"
    )