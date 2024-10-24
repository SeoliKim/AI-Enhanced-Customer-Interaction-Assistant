from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_community.llms import HuggingFacePipeline
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from order2 import OrderTrackingAgent

class CustomerSupportBot:
    def __init__(self):
        # Initialize LLAMA model from HuggingFace
        model_id = "meta-llama/Llama-2-7b-chat-hf"
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForCausalLM.from_pretrained(model_id)
        
        # Define system prompt
        system_prompt = """You are a helpful and friendly customer service assistant for an e-commerce store. 
        Your primary responsibilities are:
        1. Helping customers track their orders
        2. Providing product recommendations
        3. Assisting with visual product searches
        
        Always maintain a professional, friendly, and helpful tone. If a customer's request doesn't clearly 
        fall into one of these categories, politely guide them to choose from these options.
        
        Remember to:
        - Be concise and clear in your responses
        - Show empathy and understanding
        - Stay focused on the customer's needs
        - Provide accurate information
        - Guide customers to the right service option
        """
        
        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=512,
            temperature=0.7
        )
        
        self.llm = HuggingFacePipeline(pipeline=pipe)
        self.memory = ConversationBufferMemory()
        
        # Initialize classification prompt with system context
        self.classifier_prompt = PromptTemplate(
            input_variables=["query"],
            template=f"""
            {system_prompt}
            
            Classify the following customer support query into one of these categories:
            - Order Tracking
            - Product Recommendation
            - Visual Search
            - Other
            
            Query: {{query}}
            Classification:"""
        )
        
        self.classifier_chain = LLMChain(
            llm=self.llm,
            prompt=self.classifier_prompt,
            memory=self.memory
        )
        
        # Initialize order tracking agent
        self.order_agent = OrderTrackingAgent(self.llm)
    
    def start_conversation(self):
        return """Hi! I'm your e-commerce assistant. I can help you with:
1. Tracking your orders
2. Finding product recommendations
3. Searching products using images

How can I assist you today?"""
    
    def classify_query(self, query):
        response = self.classifier_chain.run(query=query)
        return response.strip().lower()
    
    def handle_other_category(self):
        return """I'd be happy to help! I can assist you with:
1. Order Tracking
2. Product Recommendations
3. Visual Search

Please let me know which service you'd like to use."""

def main():
    bot = CustomerSupportBot()
    
    # Start conversation
    print(bot.start_conversation())
    
    while True:
        user_input = input("User: ").strip()
        
        if user_input.lower() == 'quit':
            break
            
        # First interaction - classify the query
        category = bot.classify_query(user_input)
        
        if category == 'order tracking':
            print(bot.order_agent.request_order_number())
            order_number = input("User: ").strip()
            print(bot.order_agent.process_order(order_number))
            
        elif category == 'product recommendation':
            print("I'll help you find the perfect product! (Product recommendation logic to be implemented)")
            
        elif category == 'visual search':
            print("I can help you search using images! (Visual search logic to be implemented)")
            
        else:
            print(bot.handle_other_category())

if __name__ == "__main__":
    main()