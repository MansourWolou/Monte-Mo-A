import os
from mistralai import Mistral
import base64
from io import BytesIO
from typing import Any
from PIL.Image import Image

def format_image(image: Image) -> str:
    """
    Converts an image to a base64-encoded string with a JPEG format.

    Args:
        image (Image): The image to be formatted.

    Returns:
        str: The base64-encoded string with a data URI prefix.
    """
    # Convert image to base64
    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    # Add the prefix for base64 format
    formatted_base64 = f"data:image/jpeg;base64,{image_base64}"
    return formatted_base64


# Load Mistral API key from environment variables
api_key = os.environ["MISTRAL_API_KEY"]

# Model specification
model = "pixtral-12b-2409"

# Initialize the Mistral client
client = Mistral(api_key="JpPD7Mcbkn4kt9EASK8FyXKT0s8zdNn5")

messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "Describe the image with details in frennch"
            },
            {
                "type": "image_url",
                "image_url": format_image(df.image[1])
            }
        ]
    }
]
# Call the Mistral API to complete the chat
chat_response = client.chat.complete(
    model=model,
    messages=messages,
    response_format={
        "type": "json_object",
    }
)

# Get the content of the response
content = chat_response.choices[0].message.content

# Output the raw JSON response
print(content)