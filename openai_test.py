import openai
import os

# Use your API key
openai.api_key = os.getenv('OPENAI_API_KEY')

try:
    # List available models
    models = openai.models.list()
    for model in models.data:
        print(model.id)
except openai.OpenAIError as e:
    print(f"An error occurred: {e}")
