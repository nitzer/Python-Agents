import os
from dotenv import load_dotenv
from helpers.agent import Agent
import gradio as gr

load_dotenv()

MODEL = 'gpt-4o-mini'  # Specify the OpenAI model to use
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your-key-if-not-using-env')  # Get API key from environment or use default

agent = Agent(MODEL, OPENAI_API_KEY)
agent.set_system_message(message = "you are a helpful assistant")

agent.add_tools({
    "name": "get_ticket_price",
    "description": "Get the price of a return ticket to the destination city. Call this whenever you need to know the ticket price, for example when a customer asks 'How much is a ticket to this city'",
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "The city that the customer wants to travel to",
            },
        },
        "required": ["destination_city"],
        "additionalProperties": False
    }
})

ticket_prices = {"london": "$799", "paris": "$899", "tokyo": "$1400", "berlin": "$499"}

def get_ticket_price(destination_city):
    print(f"Tool get_ticket_price called for {destination_city}")
    city = destination_city.to_lower()
    return ticket_prices.get(city, "Unknown")

if __name__ == "__main__":
    gr.ChatInterface(fn=agent.chat, type="messages").launch()