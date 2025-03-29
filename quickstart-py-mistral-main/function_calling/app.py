import os
import logging
import functools
import json
from datetime import datetime
from mistralai import Mistral, models

logger = logging.getLogger(__name__)

api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-large-latest"

client = Mistral(api_key=api_key)

system_prompt = """
You are a highly creative and skilled poet, capable of writing poems in various styles, tones, and structures.
Your poetry must be lyrical, impactful and engaging.

Your poem must be written:
- in English the morning
- in French in the afternoon
- in Spanish in the evening.

Be angry during the week and happy during the weekend.
"""

def retrieve_weekday() -> str:
    logger.error("Retrieving the current weekday")
    print(f"Weekday: {datetime.now().strftime("%A")}")
    return f"Weekday: {datetime.now().strftime("%A")}"

def retrieve_time_of_day() -> str:
    logger.error("Retrieving the current time of day")
    current_hour = datetime.now().hour
    if current_hour < 12:
        return "Time of day: morning"
    elif current_hour < 18:
        return "Time of day: afternoon"
    return "Time of day: evening"

tools = [
    {
        "type": "function",
        "function": {
            "name": "retrieve_weekday",
            "description": "Get the current weekday",
            "parameters": {
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "retrieve_time_of_day",
            "description": "Get the current time of day",
            "parameters": {
            },
        },
    }
]

names_to_functions = {
    'retrieve_weekday': functools.partial(retrieve_weekday),
    'retrieve_time_of_day': functools.partial(retrieve_time_of_day),
}

def invoke_tool(tool_call):
    # Invoke the function called by LLM
    function_name = tool_call.function.name.lower()
    function_params = json.loads(tool_call.function.arguments)
    function_result = names_to_functions[function_name](**function_params)

    # Generate a message with role "tool"
    return {
        "role": "tool",
        "name": function_name,
        "content": function_result,
        "tool_call_id": tool_call.id,
    }

def think(prompt):
    chat_history = [
        {
            "role": "assistant",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": prompt,
        },
    ]

    # keep chatting until the LLM does not call any function
    while True:
        try:
            response = client.chat.complete(
                model=model,
                tools=tools, # list of functions that LLM might call
                tool_choice="auto", # might call a tool or not
                messages = chat_history,
                stream=False,
            )

            if response.choices[0].message.tool_calls is not None:
                # Append the function call to the current chat.
                chat_history.append(response.choices[0].message)

                # Invoke one or multiple tools
                for tool_call in response.choices[0].message.tool_calls:
                    function_result = invoke_tool(tool_call)
                    # Append the result to the current chat.
                    chat_history.append(function_result)

            # This is the final answer
            return response.choices[0].message.content

        except models.SDKError as e:
            logger.error(f"An error occurred: {e}")
            return "An error occurred. Please try again later."

def main():
    user_name = input("Please enter your name: ")
    theme = input("A theme for your poem: ")
    
    prompt = f"""Write a poem for {user_name} about {theme}.
    The poem should be 4 lines long.
    """


    response = think(prompt)
    print()
    print(response)
    print()

if __name__ == "__main__":
    main()
