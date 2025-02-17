import json
import inspect
from openai import OpenAI
from config import OPENAI_API_KEY
from db import store_expense, get_expenses_by_phone
from constants import MODEL_NAME
from toolSchemas.expenseSchema import Expense
from toolSchemas.querySchema import ExpenseQuery

class Agent:
    """
    Expense tracking bot for WhatsApp. 
    Uses OpenAI's GPT model to store and retrieve user expenses efficiently.
    """
    
    def __init__(self, open_ai_key: str):
        """Initialize the OpenAI client and define available tools for LLM interactions."""
        self.client = OpenAI(api_key=open_ai_key)
        
        # Define functions that the LLM can call
        self.bot_tools = [
            {
                "type": "function",
                "function": {
                    "name": "store_expense",
                    "description": "Store an expense record in the database.",
                    "parameters": Expense.model_json_schema(),
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_expenses_by_phone",
                    "description": "Retrieve all expense records associated with a specific phone number.",
                    "parameters": ExpenseQuery.model_json_schema(),
                },
            },
        ]

    def run_conversation(self, prompt: str) -> str:
        """
        Handles user interactions by processing input messages, invoking appropriate tools, 
        and generating responses based on stored expense data.
        """
        
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an intelligent expense tracking assistant on WhatsApp. Your job is to help users log expenses, retrieve past expenses, and provide insights on their spending habits. Keep responses concise, informative, and user-friendly. Additionally, some users may send images of their receipts. The extracted text from the image will be provided in the prompt if that is the case. This text should be used to log the expense if it is relevant to the user's expense tracking."
                ),
            },
            {"role": "user", "content": prompt},
        ]
        
        print(f"\n[INFO] Initial Message Sent: {messages}")
        
        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=self.bot_tools,
        )
        
        response_message = response.choices[0].message
        print(f"\n[INFO] Response Message Received: {response_message}")

        tool_calls = response_message.tool_calls
        if not tool_calls:
            return response_message.content  # Direct response if no function call is needed
        
        print(f"\n[INFO] Detected Tool Calls: {tool_calls}")
        
        # Mapping function names to their implementations
        available_functions = {
            "store_expense": store_expense,
            "get_expenses_by_phone": get_expenses_by_phone,
        }
        
        messages.append(response_message)

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions.get(function_name)

            if not function_to_call:
                print(f"\n[ERROR] Function '{function_name}' is not recognized.")
                continue

            function_args = json.loads(tool_call.function.arguments)

            # Dynamically match function signature parameters
            try:
                sig = inspect.signature(function_to_call)
                call_args = {
                    param: function_args.get(param, sig.parameters[param].default)
                    for param in sig.parameters
                }

                print(f"\n[INFO] Calling '{function_name}' with arguments: {call_args}")
                function_response = str(function_to_call(**call_args))

                tool_message = {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }

                print(f"\n[INFO] Appending Tool Response: {tool_message}")
                messages.append(tool_message)

            except Exception as e:
                print(f"\n[ERROR] Failed to execute '{function_name}': {e}")
                continue

        # Generate final response after function execution
        second_response = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
        )

        final_response = second_response.choices[0].message.content
        print(f"\n[INFO] Final LLM Response: {final_response}")

        return final_response
