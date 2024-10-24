from langchain_community.llms import HuggingFacePipeline
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
import sqlite3
import os

class OrderTrackingAgent:
    def __init__(self, llm):
        self.llm = llm
        self.memory = ConversationBufferMemory()
        self.db_path = '../backend/database/ecommerce_data.db'
        
        # Initialize order tracking prompt
        self.tracking_prompt = PromptTemplate(
            input_variables=["order_number"],
            template="""
            Search for order number {order_number} in the database and return its status.
            Order number: {order_number}
            Status:"""
        )
        
        self.tracking_chain = LLMChain(
            llm=self.llm,
            prompt=self.tracking_prompt,
            memory=self.memory
        )
    
    def request_order_number(self):
        return "Please provide your order number:"
    
    def get_order_status(self, order_number: str) -> str:
        if not os.path.exists(self.db_path):
            return f"Database file not found at {self.db_path}. Please check the file path."

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = """
            SELECT order_status, order_delivered_customer_date, order_estimated_delivery_date
            FROM orderDB
            WHERE order_id = ?
            """
            
            cursor.execute(query, (order_number,))
            result = cursor.fetchone()
            
            conn.close()
            
            if result:
                status, delivered_date, estimated_date = result
                
                if status.lower() == 'delivered':
                    return f"Order {order_number} status: {status}. It was delivered on {delivered_date}."
                else:
                    return f"Order {order_number} status: {status}. Estimated delivery date: {estimated_date}."
            else:
                return f"Order {order_number} not found in our database."
                
        except sqlite3.Error as e:
            return f"Database error: {str(e)}"
    
    def process_order(self, order_number):
        return self.get_order_status(order_number)