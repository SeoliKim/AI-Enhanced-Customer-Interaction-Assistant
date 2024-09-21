# AI-Enhanced-Customer-Interaction-Assistant

## Table of Contents
1. [Get Started](#get-started)
   
    Clone this repository, then follow the steps below:
    1. Install Llama-2-7B Model locally. Download the `llama-2-7b.Q4_K_M.gguf` model from the Hugging Face model hub.
        Move the downloaded model to the main directory of this project.

    2. Set Up the Virtual Environment. Open the terminal and activate the virtual environment by running:
       `source env/bin/activate`. Install the required packages by running: `pip install -r requirements.txt`.

    3. Navigate to the cli directory. Start the chatbot by running: `python3 chat_cli.py`. Be patient - it takes a little while before
       it starts running.

    5. Interact with the Chatbot. Type your queries into the terminal. The chatbot will respond with the appropriate agent to handle your 
       request.

    Example Queries:

        Where is my order?
        Find my order
        Recommend a good laptop
        Suggest a good book
        
    5. For Order Tracking, the chatbot will prompt you for your order number. It will then retrieve and display the order status along with the estimated delivery or arrival date from the database.
3. [Project Archtecture](#project-archtecture)

## Project Archtecture
