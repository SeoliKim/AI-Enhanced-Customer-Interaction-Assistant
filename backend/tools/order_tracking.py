import sqlite3
import os
from langchain_core.tools import tool
from config.config import Config

@tool
def track_order(order_number: str) -> str:
    """Track the status of an order by its order number."""
    if not os.path.exists(Config.DB_PATH):
        return f"Database file not found at {Config.DB_PATH}."
    
    try:
        conn = sqlite3.connect(Config.DB_PATH)
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
            return f"Order {order_number} status: {status}. Estimated delivery date: {estimated_date}."
        return f"Order {order_number} not found in our database."
            
    except sqlite3.Error as e:
        return f"Database error: {str(e)}"