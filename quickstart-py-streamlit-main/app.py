from mistralai import Mistral
import streamlit as st
import os

api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-large-latest"

client = Mistral(api_key=api_key)

st.title("Mistral Chat")

# Function to reset the state


def reset_state():
    for key in st.session_state:
        del st.session_state[key]


# Initialize the model in session state if it's not already set
if "mistral_model" not in st.session_state:
    st.session_state["mistral_model"] = model

# Add system prompt input
if "system_prompt" not in st.session_state:
    st.session_state["system_prompt"] = '''
You are a highly creative and skilled poet, capable of writing poems in various styles, tones, and structures.
Your poetry must be lyrical, impactful and engaging.
Write the poems in English.

Question the user to get the name of the person to whom the poem is dedicated and the theme of the poem.
'''

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": st.session_state["system_prompt"],
        }
    ]

for message in st.session_state.messages:
    if message["role"] != "system":  # Skip system messages for UI
        with st.chat_message(message["role"]):  # Use dot notation here
            st.markdown(message["content"])  # And here

if prompt := st.chat_input("Say something..."):
    new_message = {
        "role": "user",
        "content": prompt,
    }
    st.session_state.messages.append(new_message)

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        response = client.chat.complete(
            model=st.session_state["mistral_model"],
            # Pass the entire messages list
            messages=st.session_state.messages,
            stream=False,
        )
        full_response += (response.choices[0].message.content or "")
        message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": full_response,
        }
    )
