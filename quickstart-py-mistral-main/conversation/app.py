import os
from mistralai import Mistral

api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-large-latest"

client = Mistral(api_key=api_key)

system_prompt = """
You are a plumber, and you have been called to fix a leak in a customer's house.
Use your expertise to fix the leak and ensure the customer is satisfied.
Tone: Professional.
Be concise and clear in your responses.
The conversation is a multi-turn dialogue.
Speak in the same language than the user.
"""

chat_history = [
    {
        "role": "assistant",
        "content": system_prompt,
    },
]


def send_prompt_to_mistral(prompt):
    response = client.chat.complete(
        model=model,
        messages=chat_history,
        stream=False,
    )
    content = response.choices[0].message.content
    chat_history.append(
        {
            "role": "assistant",
            "content": prompt,
        }
    )
    return content


def main():
    print("Welcome to the Plumber Chatbot! Explain your issue and I will help you fix it.")
    print()

    while True:
        user_input = input("> ")
        chat_history.append(
            {
                "role": "user",
                "content": user_input,
            }
        )

        prompt = f"""Write a poem for {user_input}.
        It should be about the beauty of nature.
        The poem should be 4 lines long.
        """

        response = send_prompt_to_mistral(prompt)
        print()
        print(response)
        print()


if __name__ == "__main__":
    main()
