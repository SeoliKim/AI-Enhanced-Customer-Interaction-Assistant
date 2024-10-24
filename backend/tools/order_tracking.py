import os
from typing import Dict
from langchain_core.messages import AIMessage, HumanMessage
import sqlite3

class OrderTrackingAgent:
    def __init__(self):
        self.db_path = '../backend/database/ecommerce_data.db'
        self.waiting_for_order_number = True

    def process_query(self, state: Dict) -> Dict:
        messages = state["messages"]
        
        if self.waiting_for_order_number:
            self.waiting_for_order_number = False
            return {
                "messages": messages + [AIMessage(content="Please provide your order number.")],
                "next_agent": "order_tracking"
            }
        
        last_message = messages[-1]
        if isinstance(last_message, HumanMessage):
            order_number = last_message.content.strip()
            try:
                order_status = self.get_order_status(order_number)
            except Exception as e:
                order_status = f"An error occurred while retrieving the order status: {str(e)}"
            self.waiting_for_order_number = True  # Reset for next interaction
            
            return {
                "messages": messages + [AIMessage(content=order_status)],
                "next_agent": "router"
            }
        else:
            return {
                "messages": messages + [AIMessage(content="I'm sorry, I didn't receive a valid order number. Please try again.")],
                "next_agent": "order_tracking"
            }

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

def create_order_tracking_agent():
    return OrderTrackingAgent()