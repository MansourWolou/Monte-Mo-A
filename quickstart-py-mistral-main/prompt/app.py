import os
from mistralai import Mistral

api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-large-latest"

client = Mistral(api_key=api_key)

system_prompt = """
You are a highly creative and skilled poet, capable of writing poems in various styles, tones, and structures.
Your poetry must be lyrical, impactful and engaging.
Write the poems in English.
"""

def send_prompt_to_mistral(prompt):
    response = client.chat.complete(
        model=model,
        messages = [
            {
                "role": "assistant",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        stream=False,
    )
    return response.choices[0].message.content

def main():
    user_name = input("Please enter your name: ")
    theme = input("A theme for your poem: ")
    
    prompt = f"""Write a poem for {user_name} about {theme}.
    The poem should be 4 lines long.
    """

    response = send_prompt_to_mistral(prompt)
    print()
    print(response)
    print()

if __name__ == "__main__":
    main()
