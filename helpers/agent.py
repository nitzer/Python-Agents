from openai import OpenAI
from typing import Dict, Text

class Agent:
    def __init__(self, model, api_key):
        self.messages = []
        self.model = model
        self.tools = []
        self.openai = OpenAI(api_key=api_key)

    def add_tool(self, tool: Dict):
        self.tools.append({"type": "function", "function": tool})

    def set_message(self, content, role="user"):
        self.messages.append({"role": role, "content": content})

    def set_raw_messages(self, messages):
        # This will replace the current messages
        self.messages = messages

    def debug(self):
        print(self.messages)

    def get_response(self):
        response = self.openai.chat.completions.create(
            model=self.model,
            messages = self.messages
        )

        if response.choices:
            return response.choices[0].message.content
        else:
            return "I don't know..."
    
    def set_system_message(self, message):
        self.system_message = message
    
    def stream_chat(self, message, history):
        messages = [{"role": "system", "content": self.system_message}] + history + [{"role": "user", "content": message}]
        stream = self.openai.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=self.tools,
            stream=True
        )
        response = ""
        for chunk in stream:
            response += chunk.choices[0].delta.content or ''
            yield response
    
    def chat(self, message, history):
        messages = [{"role": "system", "content": self.system_message}] + history + [{"role": "user", "content": message}]
        response = self.openai.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=self.tools,
        )

        if response.choices[0].finish_reason=="tool_calls":
            message = response.choices[0].message
            response, city = self.handle_tool_call(message)
            self.messages.append(message)
            self.messages.append(response)
            response = self.openai.chat.completions.create(model=self.model, messages=self.messages)
            
        return response.choices[0].message.content

    def get_stream_response(self):
        stream = self.openai.chat.completions.create(model=self.model, messages=self.messages, stream=True)
        response = ""
        for chunk in stream:
            response += chunk.choices[0].delta.content or ''
            yield response