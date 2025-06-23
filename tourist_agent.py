import os
from dotenv import load_dotenv
import gradio as gr
from helpers.tourist_agent import TourismAgent

load_dotenv()

MODEL = 'gpt-4o-mini'  # Specify the OpenAI model to use
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your-key-if-not-using-env')  # Get API key from environment or use default

agent = TourismAgent(model=MODEL,api_key=OPENAI_API_KEY)

if __name__ == "__main__":
    gr.ChatInterface(fn=agent.chat, type="messages").launch()