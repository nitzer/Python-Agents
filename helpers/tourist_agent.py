from .agent import Agent
import json

class TourismAgent(Agent):
    agent_tools = {
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
    }

    personality = """you are a helpful assistant
    Give short, courteous answers, no more than 1 sentence.
    Always be accurate. If you don't know the answer, say so.
    """

    ticket_prices = {"london": "$799", "paris": "$899", "tokyo": "$1400", "berlin": "$499"}

    def __init__(self, model, api_key):
        super().__init__(model=model, api_key=api_key)
        super().add_tool(self.agent_tools)
        super().set_system_message(message=self.personality)

    def handle_tool_call(self, message):
        tool_call = message.tool_calls[0]
        arguments = json.loads(tool_call.function.arguments)
        if (tool_call.function.name == 'get_ticket_price'):
            city = arguments.get('destination_city')
            price = self.get_ticket_price(city)
            response = {
                "role": "tool",
                "content": json.dumps({"destination_city": city,"price": price}),
                "tool_call_id": tool_call.id
            }
            return response, city
        
        return ''

    def get_ticket_price(self, destination_city):
        print(f"Tool get_ticket_price called for {destination_city}")
        city = destination_city.lower()
        return self.ticket_prices.get(city, "Unknown")