# 4. tools/product_recommendations.py
import sqlite3
from typing import List, Dict, Any
from langchain_core.tools import tool
from backend.config.config import Config

@tool
def get_product_recommendations(user_id: str, category: str = None) -> List[Dict[str, Any]]:
    """Get personalized product recommendations for a user."""
    try:
        conn = sqlite3.connect(Config.DB_PATH)
        cursor = conn.cursor()
        
        query = """
        SELECT p.product_id, p.name, p.description, p.price, p.category
        FROM productsDB p
        JOIN user_preferences up ON p.category = up.preferred_category
        WHERE up.user_id = ?
        """
        params = [user_id]
        
        if category:
            query += " AND p.category = ?"
            params.append(category)
            
        query += " ORDER BY up.preference_score DESC LIMIT 5"
        
        cursor.execute(query, params)
        columns = ['product_id', 'name', 'description', 'price', 'category']
        recommendations = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return recommendations
        
    except sqlite3.Error as e:
        return f"Database error: {str(e)}"