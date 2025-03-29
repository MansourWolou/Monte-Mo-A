import os
from mistralai import Mistral
from pydantic import BaseModel

api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-large-latest"

client = Mistral(api_key=api_key)


class Color(BaseModel):
    rgb: str
    name: str
    variants: list[str]


response = client.chat.parse(
    model=model,
    messages=[
        {
            "role": "system",
            "content": "Extract the right color."
        },
        {
            "role": "user",
            "content": "Roses are red, violets are:"
        },
    ],
    response_format=Color,
)

print(response.choices[0].message.parsed)
