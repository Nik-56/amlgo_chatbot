
import dotenv
import os
dotenv.load_dotenv()

from google import genai
from google.genai import types


def get_chatbot_response(message, system_instruction=None):

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=message,
        config=types.GenerateContentConfig(
            temperature=0.1,
            system_instruction=system_instruction,
            max_output_tokens=2000
        )
    ).text
    return response



# to get embeddings
import requests
import json
import os
from google import genai
from google.genai import types

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_embeddings(user_input):
    result = client.models.embed_content(
    model="text-embedding-004",
    contents=user_input,
    config=types.EmbedContentConfig(output_dimensionality=768),
    )
    values = result.embeddings[0].values
    return values

