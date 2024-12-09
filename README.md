# AI Enhanced Customer Interaction Assistant

## Table of Contents
- [Overview](#overview)
- [Business Impact](#business-impact)
- [Quick Start](#quick-start)
- [Build With](#build-with)
- [Acknowledgements](#acknowledgements)

## Overview

This advanced AI-powered solution leverages multi-agent framework to revolutionize e-commerce platforms. It is designed to enhance customer engagement and streamline interactions by providing:

- **Real-Time Assistance**: Respond to customer inquiries instantly with intelligent, context-aware support.
- **Personalized Product Recommendations**: Offer tailored suggestions based on customer preferences and behavior.
- **Dynamic Order Tracking**: Enable seamless, up-to-date tracking of orders with precise updates.
- **Visual Search Capabilities**: Allow customers to search for products using images for an intuitive shopping experience.

## Business Impact
#### Addressing Evolving Manufacturing Needs
- **Increasing Customer Expectations**  
  The competitive e-commerce landscape demands **24/7**, **personalized**, and **efficient customer support** to meet rising consumer needs.  
  Traditional customer service methods are no longer sufficient to handle these heightened expectations effectively.

#### Strategic Opportunity
- **AI-Driven Automation**  
  Automating routine interactions with AI reduces operational costs and improves efficiency, allowing businesses to allocate resources more strategically.

- **Personalized Customer Engagement**  
  Leveraging AI for tailored recommendations enhances customer engagement and drives sales by creating a more interactive and satisfying shopping experience.

## Quick Start

To showcase this project

1. Clone the repository:
   ```bash
    git clone https://github.com/SeoliKim/AI-Enhanced-Customer-Interaction-Assistant.git
   ```

2. Create a virtual environment:
   ```bash
    python3 -m venv env
    source env/bin/activate
   ```

3. Install the required packages:
   ```bash
    pip install -r requirements.txt
    ```

4. Build the database
    ```bash
     cd backend/database
     python3 database_setup.py
    ```

5. Edit the `config.py` file in the `backend` directory to include your own API keys for OpenAI API and other configurations if desired. 

6. Run the assistant
    ```bash
    cd frontend
    mesop main.py
    ```
7. Open the link `http://localhost:32123` in your browser to interact with the assistant.

## Demo
See a live demonstration of the AI Enhanced Customer Interaction Assistant:
[demo](./demo.mp4)
## Build With
- **Frontend**: Mesop, Python
- **Backend**: Langgraph, Langchain, Python, tool-binding, OpenAI API
- **AI Algorithms**: YOLOv3, OpenAI API, word embeddings, Tfidf vectorizera
- **Database**: SQLite

## Acknowledgements
We extend our heartfelt gratitude to our advisors, **Hiwot Sidelil** and **Muntasir AL Kabir** from DXC Technology, for their pivotal role in defining the project's objectives and offering crucial insights into industrial practices and technical integration. Their guidance and support have been instrumental in the successful development of this project.

Additionally, thank you to Break Through Tech, the Cornell Tech AI Program team, and especially Erika and Veronica for providing this opportunity to collaborate with DXC Technology!