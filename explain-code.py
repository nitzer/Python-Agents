import os
from dotenv import load_dotenv
from helpers.agent import Agent
import gradio as gr

load_dotenv()

MODEL = 'gpt-4o-mini'  # Specify the OpenAI model to use
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your-key-if-not-using-env')  # Get API key from environment or use default

agent = Agent(MODEL, OPENAI_API_KEY)

def check_code(system_prompt, message):
    agent.set_message(system_prompt, "system")
    agent.set_message(message)
    return agent.get_response()

if __name__ == "__main__":
    default_system_prompt = "You are an expert Software Engineer and that explains code to people that are learning"

    view = gr.Interface(fn=check_code, inputs=[
        gr.Textbox(label="System prompt", value=default_system_prompt),
        gr.Textbox(label="Paste the code you want to analyze:", lines=6)
    ], outputs=[
        gr.Markdown(label="Here's your output:")
    ])
    view.launch()