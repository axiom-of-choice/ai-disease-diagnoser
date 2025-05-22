import os
from openai import OpenAI
from config import OPENAI_API_KEY

# Create a single client instance
client = OpenAI(api_key=OPENAI_API_KEY)
